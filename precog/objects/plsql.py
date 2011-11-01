from precog import db
from precog.diff import Diff, PlsqlDiff, Reference
from precog.errors import PlsqlSyntaxError, PrecogError
from precog.objects._assert import *
from precog.objects._misc import *
from precog.objects.base import OracleObject
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

  def diff (self, other):
    diffs = super().diff(other)

    if not diffs:
      errors = other.errors()
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

  def errors (self):
    rs= db.query(""" SELECT line
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
      self.log.warn(PlsqlSyntaxError(warnings))

    if errors:
      raise PlsqlSyntaxError(self, errors)

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT text
                      FROM dba_source
                      WHERE owner = :o
                        AND name = :n
                        AND type = :t
                      ORDER BY line
                  """, o=name.schema, n=name.obj, t=class_.type)
    if not rs:
      into_database.log.warn("PL/SQL source not found for {}".format(name))
      return None
    return class_(name, source=''.join(row['text'] for row in rs),
        database=into_database)

class PlsqlHeader (PlsqlCode):
  pass

class PlsqlBody (HasProp('header', dependency=Reference.AUTODROP,
                         assert_type=PlsqlHeader),
                 PlsqlCode):

  @classmethod
  def from_db (class_, name, into_database):
    body = super().from_db(name, into_database)
    header_class = _type_to_class(class_.type.split()[0], name)
    body.header = into_database.find(body.name, header_class)

    return body

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
