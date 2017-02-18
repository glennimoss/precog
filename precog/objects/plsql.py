import difflib, re
from precog import db
from precog.diff import Diff, ErrorCheckingDiff, PlsqlDiff, Reference
from precog.errors import (NonexistentSchemaObjectError, PlsqlSyntaxError,
                           PrecogError, UnimplementedFeatureError)
from precog.objects.base import OracleObject, OracleFQN
from precog.objects.has.prop import HasProp
from precog.util import _type_to_class_name, _with_location

def _type_to_class (type, name):
  try:
    return globals()[_type_to_class_name(type)]
  except KeyError as e:
    raise PrecogError(
      '{} [{}]: unexpected PL/SQL type'.format(type, name)) from e

_volatile_pat = re.compile(r'--@\s*volatile\s*$', re.I)
_volatile = lambda s: _volatile_pat.search(s)

class PlsqlCode (OracleObject):

  def __init__ (self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.unified_diff = None

  @staticmethod
  def new (type, name, source, **props):
    # Create object of subclass, based on the Oracle type passed in
    class_ = _type_to_class(type, name)
    return class_(name, source=source, **props)

  def _sql (self, fq=True):
    return self.props['source']

  def create (self):
    return PlsqlDiff('CREATE OR REPLACE {}'.format(self.sql()), produces=self,
                     priority=Diff.CREATE)

  def _diff_props (self, other):
    prop_diff = super()._diff_props(other)

    if 'source' in prop_diff:
      sourcediff = list(difflib.unified_diff(other.props['source'].splitlines(),
                                             self.props['source'].splitlines(),
                                             _with_location(other),
                                             _with_location(self), lineterm=''))
      # Look to see if the the only changes have --@ volatile and ignore diffs
      # only containing these volatile changes. Useful for things like
      # svn:keywords $Id$ etc.
      adds = [line for line in sourcediff[2:] if line[0] == '+']
      subs = [line for line in sourcediff[2:] if line[0] == '-']
      if len(adds) == len(subs) and not [1 for line in adds
                                         if not _volatile(line)]:
        del prop_diff['source']

      self.unified_diff = ''.join('-- {}\n'.format(diffline)
                                  for diffline in sourcediff)

    return prop_diff

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)

    if not diffs:
      errors = other.errors(False)
      if errors:
        diffs.extend(self.rebuild())

    return diffs

  def recreate (self, other):
    return [self.create()]

  def rebuild (self, plsql_type=None, extra_parameters=None):
    if not plsql_type:
      plsql_type = self.type
    parts = ['ALTER', plsql_type, self.name, 'COMPILE']
    if extra_parameters:
      parts.append(extra_parameters)
    parts.append('REUSE SETTINGS')

    return [ErrorCheckingDiff(' '.join(parts), produces=self)]

  def errors (self, throw=True):
    rs = db.query_all(""" SELECT line
                               , position
                               , text
                               , attribute
                          FROM dba_errors
                          WHERE owner = :o
                            AND name = :n
                            AND type = :t
                          ORDER BY sequence
                      """, o=self.name.schema, n=self.name.obj, t=self.type)
    warnings = [row for row in rs if row['attribute'] == 'WARNING']
    errors = [row for row in rs if row['attribute'] == 'ERROR']

    if warnings:
      self.log.warn(PlsqlSyntaxError(self, warnings))

    if errors:
      e = PlsqlSyntaxError(self, errors)
      if throw:
        raise e
      self.log.error(e)

  @classmethod
  def from_db (class_, schema, into_database, plsql_names=None):
    plsql_filter = db.filter_clause("object_type || '.' || object_name",
                                    plsql_names)
    into_database.log.debug("Querying for plsql {} from DB...".format(
      "(all)" if plsql_names is None else ", ".join(plsql_names)))
    rs = db.query(""" SELECT do.object_name
                           , do.object_type
                           , do.status
                           , CURSOR(SELECT ds.text
                                    FROM dba_source ds
                                    WHERE ds.owner = do.owner
                                      AND ds.name = do.object_name
                                      AND ds.type = do.object_type
                                    ORDER BY ds.line
                             ) AS text
                      FROM dba_objects do
                      WHERE do.owner = :o
                        AND do.object_type IN ( 'FUNCTION'
                                              , 'PACKAGE'
                                              , 'PACKAGE BODY'
                                              , 'PROCEDURE'
                                              , 'TRIGGER'
                                              , 'TYPE'
                                              , 'TYPE BODY'
                                              )
                        -- Ignore secretly generated types for PL/SQL types
                        AND do.object_name NOT LIKE 'SYS_PLSQL%' -- PLSQL function generated types
                        AND do.object_name NOT LIKE 'SYSTPS%==' -- Collection types generated by COLLECT()
                         {}
                  """.format(plsql_filter), o=schema,
                  oracle_names=['object_name'])

    into_database.log.debug("Cursor obtained")
    for row in rs:
      plsql_name = OracleFQN(schema, row['object_name'])
      into_database.log.debug("Processing plsql {}".format(plsql_name))
      yield _type_to_class(row['object_type'], plsql_name)(
        plsql_name, source=''.join(line['text'] for line in row['text']),
        database=into_database, create_location=(db.location,),
        status=row['status'])

    filter_clause = ''
    if plsql_names:
      dep_filter = db.filter_clause("type || '.' || name", plsql_names, logical_connective="AND (")
      ref_filter = db.filter_clause("referenced_type || '.' || referenced_name", plsql_names, logical_connective="OR")
      filter_clause = '{} {})'.format(dep_filter, ref_filter)

    into_database.log.debug("Querying for plsql {} dependencies from DB...".format(
      "(all)" if plsql_names is None else ", ".join(plsql_names)))
    rs = db.query(""" SELECT name
                           , type
                           , dependency_type
                           , referenced_owner
                           , referenced_name
                           , referenced_type
                      FROM dba_dependencies
                      WHERE owner = :o
                        AND type IN ( 'TYPE', 'TABLE' /*'FUNCTION'
                                    , 'PACKAGE'
                                    , 'PACKAGE BODY'
                                    , 'PROCEDURE'
                                    , 'TRIGGER'
                                    , 'TYPE'
                                    , 'TYPE BODY' */
                                    )
                        AND referenced_type = 'TYPE'
                        AND referenced_owner NOT IN ('SYS', 'PUBLIC')
                        {}
                      ORDER BY type, name
                  """.format(filter_clause), o=schema,
                  oracle_names=['name', 'referenced_owner', 'referenced_name'])
    into_database.log.debug("Cursor obtained")
    for row in rs:
      if row['dependency_type'] != 'HARD':
        raise UnimplementedFeatureError("Unsupported dependency_type = {}".format(row['dependency_type']))

      name = OracleFQN(schema, row['name'])
      try:
        obj = into_database.find(name, row['type'], deferred=False)

        referenced_name = OracleFQN(row['referenced_owner'], row['referenced_name'])
        referenced_obj = into_database.find(referenced_name, row['referenced_type'])

        into_database.log.debug("{} depends on {}".format(obj.pretty_name, referenced_obj.pretty_name))
        obj._set_dependency(referenced_obj)
      except NonexistentSchemaObjectError:
        # If we don't know about the object, we don't want to track its dependencies
        pass


class PlsqlHeader (PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    if not self.deferred:
      try:
        body_class = _type_to_class(type(self).type + ' BODY', self.name)
        body = self.database.find(self.name, body_class, deferred=False)
        body.header = self
      except NonexistentSchemaObjectError:
        pass

  def rebuild(self):
    return super().rebuild(extra_parameters='SPECIFICATION')

class PlsqlBody (HasProp('header', dependency=Reference.AUTODROP,
                         assert_type=PlsqlHeader),
                 PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    if not self.deferred and not self.header:
      try:
        header_class = _type_to_class(type(self).type.split()[0], self.name)
        self.header = self.database.find(self.name, header_class,
                                         deferred=False)
      except NonexistentSchemaObjectError:
        pass

  def _eq_header (self, other):
    # We don't want to fail just because our headers differ in text
    return True

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)

    if not diffs and self.header != other.header:
      diffs.extend(self.rebuild())

    return diffs

class Function (PlsqlCode):
  pass

class Procedure (PlsqlCode):
  pass

class Package (PlsqlHeader):
  pass

class PackageBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('PACKAGE', 'BODY')

class Trigger (PlsqlCode):
  pass

class Type (PlsqlHeader):
  def recreate (self, other):
    create = self.create()
    teardowns = other.teardown()
    create.add_dependencies(teardowns)
    rebuild = other.build_up()
    for diff in rebuild:
      diff.add_dependencies(create)
    diffs = teardowns + [create] + rebuild
    return diffs

class TypeBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('TYPE', 'BODY')
