import difflib, re
from precog import db
from precog.diff import Diff, ErrorCheckingDiff, PlsqlDiff, Reference
from precog.errors import PlsqlSyntaxError, PrecogError
from precog.objects._assert import *
from precog.objects._misc import *
from precog.objects.base import OracleObject, OracleFQN
from precog.objects.has.prop import HasProp
from precog.util import HasLog

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
      sourcediff = [line for line in
                    difflib.unified_diff(other.props['source'].splitlines(),
                                         self.props['source'].splitlines(),
                                         _with_location(other),
                                         _with_location(self), lineterm='')]
      # Look to see if the the only changes have --@ volatile and ignore diffs
      # only containing these volatile changes. Useful for things like
      # svn:keywords $Id$ etc.
      if not [1 for line in sourcediff[2:]
              if line[0] == '+' and not _volatile(line)]:
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
                        AND object_type IN ( 'FUNCTION'
                                           , 'PACKAGE'
                                           , 'PACKAGE BODY'
                                           , 'PROCEDURE'
                                           , 'TRIGGER'
                                           , 'TYPE'
                                           , 'TYPE BODY'
                                           )
                         {}
                  """.format(plsql_filter), o=schema,
                  oracle_names=['object_name'])

    for row in rs:
      plsql_name = OracleFQN(schema, row['object_name'])
      yield _type_to_class(row['object_type'], plsql_name)(
        plsql_name, source=''.join(line['text'] for line in row['text']),
        database=into_database, create_location=(db.location,),
        status=row['status'])
    rs.close()

class PlsqlHeader (PlsqlCode):

  def rebuild(self):
    return super().rebuild(extra_parameters='SPECIFICATION')

class PlsqlBody (HasProp('header', dependency=Reference.AUTODROP,
                         assert_type=PlsqlHeader),
                 PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    if not self.header:
      header_class = _type_to_class(type(self).type.split()[0], self.name)
      self.header = self.database.find(self.name, header_class)

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
  pass

class TypeBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('TYPE', 'BODY')
