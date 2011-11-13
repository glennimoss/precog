from precog import db
from precog.diff import Diff, PlsqlDiff, Reference
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
        "{} [{}]: unexpected PL/SQL type".format(type, name)) from e

class PlsqlCode (OracleObject):

  @staticmethod
  def new (type, name, source, **props):
    # Create object of subclass, based on the Oracle type passed in
    class_ = _type_to_class(type, name)
    return class_(name, source=source, **props)

  def _sql (self, fq=True):
    return "CREATE OR REPLACE {}".format(self.props['source'])

  def create (self):
    return [PlsqlDiff(self.sql(), produces=self, priority=Diff.CREATE)]

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)

    if not diffs:
      errors = other.errors(False)
      if errors:
        diffs.extend(self.rebuild())

    return diffs

  def recreate (self, other):
    return self.create()

  def rebuild (self, plsql_type=None, extra_parameters=None):
    if not plsql_type:
      plsql_type = self.type
    parts = ['ALTER', plsql_type, self.name, 'COMPILE']
    if extra_parameters:
      parts.append(extra_parameters)
    parts.append("REUSE SETTINGS")

    return [PlsqlDiff(" ".join(parts), produces=self, terminator=';')]

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
  def from_db (class_, schema, into_database):
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
                  """, o=schema, oracle_names=['object_name'])

    for row in rs:
      plsql_name = OracleFQN(schema, row['object_name'])
      yield _type_to_class(row['object_type'], plsql_name)(
        plsql_name, source="".join(line['text'] for line in row['text']),
        database=into_database, create_location=(db.location,),
        status=row['status'])
    rs.close()

class PlsqlHeader (PlsqlCode):
  pass

class PlsqlBody (HasProp('header', dependency=Reference.AUTODROP,
                         assert_type=PlsqlHeader),
                 PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    if not self.header:
      header_class = _type_to_class(type(self).type.split()[0], self.name)
      self.header = self.database.find(self.name, header_class)

class Function (PlsqlCode):
  pass

class Procedure (PlsqlCode):
  pass

class Package (PlsqlHeader):

  def rebuild(self):
    return super().rebuild(extra_parameters='SPECIFICATION')

class PackageBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('PACKAGE', 'BODY')

class Trigger (PlsqlCode):
  pass

class Type (PlsqlHeader):

  def rebuild(self):
    return super().rebuild(extra_parameters='SPECIFICATION')

class TypeBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('TYPE', 'BODY')
