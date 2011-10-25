from precog.objects._assert import *
from precog.objects._misc import *
from precog.objects.base import OracleObject

def _in_props (*foo):
  return property()

class PlsqlCode (OracleObject):

  @staticmethod
  def new (type, name, source, **props):
    # Create object of subclass, based on the Oracle type passed in
    try:
      class_ = _type_to_class(type)
      if not issubclass(class_, PlsqlCode):
        raise _UnexpectedTypeError()
      return class_(name, source=source, **props)
    except _UnexpectedTypeError:
      self.log.warn("{} [{}]: unexpected PL/SQL type".format(
        class_name, obj['object_name']))
      raise

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
      return None
    return class_(name, source=''.join(row['text'] for row in rs),
        database=into_database)

class PlsqlHeader (PlsqlCode):
  pass

class PlsqlBody (PlsqlCode):

  _header = _in_props('header')

  @_header.setter
  def header (self, value):
    _assert_type(value, PlsqlHeader)
    self._depends_on(value, '_header', Reference.AUTODROP)

  @classmethod
  def from_db (class_, name, into_database):
    body = super().from_db(name, into_database)
    header_class = _type_to_class(class_.type.split()[0])
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

  def diff (self, other):
    if self != other:
      return self.recreate(other)
    else:
      return super().diff(other)

  def rebuild(self):
    return super().rebuild(extra_parameters='SPECIFICATION')

class TypeBody (PlsqlBody):

  def rebuild(self):
    return super().rebuild('TYPE', 'BODY')
