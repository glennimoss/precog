import re

import cx_Oracle
import reserved
from coercecmp import coerced_comparison

class InsensitiveDict (dict):

  def __setitem__ (self, key, value):
    if isinstance(key, str):
      key = key.upper()

    super().__setitem__(key, value)

  def __getitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    return super().__getitem__(key)

  def __delitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    super().__delitem__(key)

  def __contains__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    return super().__contains__(key)

class DBManager (object):

  def __init__ (self):
    self.connection = cx_Oracle.connect('gim', 'abc123', 'tkboi')
    self.curs = self.connection.cursor()

  def query (self, *args, **kvargs):
    self.curs.execute(*args, **kvargs)
    return [InsensitiveDict(
              zip((column[0] for column in self.curs.description), row)
            ) for row in self.curs]

  def execute (self, *args, **kvargs):
    self.curs.execute(*args, **kvargs)

    return self.curs.rowcount

db = DBManager()

class TypeConflict (Exception):

  def __init__ (self, obj, wrongtype='a different type'):
    self.obj = obj
    self.wrongtype = wrongtype

  def __str__ (self):
    return "TypeConflict: {} [{}] exists as {}".format(
        self.obj.type(), self.obj.name, self.wrongtype) 

class OracleNameError (Exception):
  pass

@coerced_comparison
class OracleIdentifier (str):

  def __new__ (self, identifier):
    identifier = str(identifier)
    quoted = identifier.startswith('"') and identifier.endswith('"')
    identifier = identifier
    if not quoted:
      identifier = identifier.upper()

    if len(identifier) == (0 if not quoted else 2):
      raise OracleNameError("Object name cannot be empty")

    if identifier in reserved.words:
      raise OracleNameError(
        "Object name {} is a reserved word".format(repr(identifier)))

    if len(identifier) > (30 if not quoted else 32):
      raise OracleNameError(
        "Object name {} is longer than 30 characters"
        .format(repr(identifier)))

    if (not quoted and 
        not re.match('^[A-Z_$#][0-9A-Z_$#]*$', identifier)):
      raise OracleNameError(
        "Object name {} must not start with a number and "
        "otherwise contain only letters, numbers, _, $, or #"
        .format(repr(identifier)))

    if (quoted and 
        not re.match('^"[^"\0]+"$', identifier)):
      raise OracleNameError(
        "Quoted object name {} cannot contain \" or \\0"
        .format(repr(identifier)))

    return super().__new__(self, identifier)

  def __repr__ (self):
    return "OracleIdentifier({})".format(super().__repr__())

class OracleFQN (object):
  def __init__ (self, schema=None, obj=None, part=None):
    self.schema = schema
    self.obj = obj
    self.part = part

    if not self.obj:
      raise Exception('have to have a name')

  def __str__ (self):
    return '.'.join(x for x in (self.schema, self.obj, self.part) if x)

class OracleObject (object):

  def __init__ (self, name):
    self.name = OracleIdentifier(name)
    self.props = InsensitiveDict()

  def type(self):
    return type(self).__name__.upper()

  def __str__ (self):
    return self.sql()

  def exists (self):
    rs = db.query(
        """ SELECT object_name, object_type
            FROM user_objects 
            WHERE object_name = :name
        """, name=self.name)

    if not rs:
      return False

    rs = rs[0]
    if rs['object_type'] != self.type():
      raise TypeConflict(self, rs['object_type'])

    return True

  def create (self):
    if not self.exists():
      return db.execute(self.sql())

  def drop (self):
    if self.exists():
      return db.execute("DROP {} {}".format(self.type(), self.name))

  """ This is probably too powerful
  def force (self):
    try:
      return self.create()
    except TypeConflict as e:
      db.execute("DROP {} {}".format(e.wrongtype, self.name))
      return self.create()
  """





class Table (OracleObject):

  def __init__ (self, name, columns):
    super().__init__(name)
    self.columns = []
    for c in columns:
      self.columns.append(Column(*c, table=self))

  def sql (self):
    return "CREATE TABLE {} (\n    {}\n  )".format(self.name, 
        ',\n    '.join(c.sql() for c in self.columns))

  def exists (self):
    exists = super().exists()

    if exists:
      for c in self.columns:
        exists &= c.exists()

    return exists

class DataTypeConflict (TypeConflict):

  def __init__ (self, obj, diff_props):
    super().__init__(obj)
    self.diff_props = diff_props

  def __str__ (self):
    return (
        "DataTypeConflict: {} [{}]:\n  "
          .format(self.obj.type(), self.obj.fqn) +
        "\n  ".join("{} = {} but found {}".format(
            prop, self.obj.props[prop], found) 
          for prop, found in self.diff_props.items()))
           

class Column (OracleObject):

  def __init__ (self, name, datatype, length=None, table=None):
    super().__init__(name)
    self.props['data_type'] = datatype.upper()
    if length is not None:
      self.props['data_length'] = int(length)
    self.table = table
    self.fqn = OracleFQN(obj=self.table.name, part=self.name)

  def sql (self):
    data_type = self.props['data_type']
    if 'data_length' in self.props:
      data_type += "({})".format(self.props['data_length'])
    return "{} {}".format(self.name, data_type)

  def exists (self):
    rs = db.query(
        """ SELECT {}
            FROM user_tab_cols
            WHERE table_name = :tab
              AND column_name = :col
        """.format(', '.join(self.props.keys())), 
        tab=self.table.name, col=self.name)

    if not rs:
      return False

    rs = rs[0]
    diff = {prop: rs[prop] for prop, expected in self.props.items() 
              if expected != rs[prop]}

    if diff:
      raise DataTypeConflict(self, diff)

    return True

if __name__ == '__main__':
  db = DBManager()

  rs = db.query('select * from foop')

  print(rs[0]['VALUE'])
