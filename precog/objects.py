import re

from precog.errors import *
from precog.util import coerced_comparison, InsensitiveDict
from precog import db
from precog import reserved

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
    self.schema = OracleIdentifier(schema) if schema else None
    self.obj = OracleIdentifier(obj) if obj else None
    self.part = OracleIdentifier(part) if part else None

    if not (self.schema or self.obj or self.part):
      raise OracleNameError('have to have a name')

  def __str__ (self):
    return '.'.join(x for x in (self.schema, self.obj, self.part) if x)

  def __repr__ (self):
    return "OracleFQN({})".format(', '.join(
        "{}='{}'".format(arg, val) for arg, val in
          (('schema', self.schema), ('obj', self.obj), ('part', self.part))
          if val))

  def __hash__ (self):
    return self.__str__().__hash__()

  def __eq__ (self, other):
    if not isinstance(other, OracleFQN):
      return False

    return (self.schema == other.schema and
            self.obj == other.obj and
            self.part == other.part)




class OracleObject (object):

  def __init__ (self, name):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name
    self.props = InsensitiveDict()
    self.type = type(self).__name__.upper()

  def __str__ (self):
    return self.sql()

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    if self.name != other.name:
      return False

    return True

  def exists (self):
    rs = db.query(
        """ SELECT object_type
            FROM all_objects
            WHERE owner = :o
              AND object_name = :n
              AND object_type = :t
        """, o=self.name.schema, n=self.name.obj, t=self.type)

    if not rs:
      return False

    rs = rs[0]
    if rs['object_type'] != self.type:
      raise TypeConflict(self, rs['object_type'])

    return True

  def diff (self):
    if not self.exists():
      return [self.sql()]

    return []

  def drop (self):
    if self.exists():
      return db.execute("DROP {} {}".format(self.type, self.name))

  """ This is probably too powerful
  def force (self):
    try:
      return self.create()
    except TypeConflict as e:
      db.execute("DROP {} {}".format(e.wrongtype, self.name))
      return self.create()
  """





class Table (OracleObject):

  def __init__ (self, name, columns=[]):
    super().__init__(name)
    self.columns = []
    for c in columns:
      if not isinstance(c, Column):
        c = Column(*c, table=self)
      else:
        c.table = self
      self.columns.append(c)

  def __repr__ (self):
    return ("Table('" + self.name.obj + "', [" +
        ', '.join(repr(c) for c in self.columns) + '])')

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycols = {c.name: c for c in self.columns}
    othercols = {c.name: c for c in other.columns}

    return mycols == othercols


  def sql (self):
    return "CREATE TABLE {} (\n    {}\n  )".format(self.name,
        ',\n    '.join(c.sql() for c in self.columns))

  def exists (self):
    exists = super().exists()

    """ Not sure if we want to do this
    if exists:
      for c in self.columns:
        exists &= c.exists()
    """

    return exists

  def diff (self):
    diffs = []
    if self.exists():
      for c in self.columns:
        diff = c.diff()
        if diff:
          diffs.extend(diff)
    else:
      diffs.append(self.sql())

    return diffs

  @staticmethod
  def fromDb (name):



class Column (OracleObject):

  def __init__ (self, name, data_type, data_length=None, data_precision=None,
      data_scale=None, table=None):
    super().__init__(OracleFQN(part=name))
    self.props['data_type'] = data_type.upper()
    if data_length is not None:
      self.props['data_length'] = int(data_length)
    if data_precision is not None:
      self.props['data_precision'] = int(data_precision)
    if data_scale is not None:
      self.props['data_scale'] = int(data_scale)

    if table:
      self.table = table
      self.name.schema = table.name.schema
      self.name.obj = table.name.obj
    #self.fqn = OracleFQN(obj=self.table.name, part=self.name)

  def __repr__ (self):
    return ("Column('" + self.name.part + "', " +
        ', '.join(prop.lower() + '=' + repr(val)
          for prop, val in self.props.items()) + ')')

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    if self.props != other.props:
      return False

    return True


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
    diff = InsensitiveDict((prop, rs[prop])
        for prop, expected in self.props.items() if expected != rs[prop])

    if diff:
      raise DataTypeConflict(self, diff)

    return True

  def diff (self):
    diffs = []
    try:
      if not self.exists():
        diffs.append("ALTER TABLE {} ADD ( {} )".format(
          self.table.name, self.sql()))
    except DataTypeConflict as e:
      if ('data_type' in e.diff_props) or ('data_length' in e.diff_props):
        diffs.append("ALTER TABLE {} MODIFY ( {} )".format(
          self.table.name, self.sql()))

    return diffs


class Constraint (OracleObject):

  def __init__ (self, name, table=None):
    super().__init__(name)
    self.table = table

class Index (OracleObject):
  pass

class Sequence (OracleObject):
  pass

class Synonym (OracleObject):
  pass

class Grant (OracleObject):
  pass

class View (OracleObject): # Table??
  pass

class PlsqlCode (OracleObject):
  pass

#######################################
# PL/SQL Code Objects
#######################################
class Function (PlsqlCode):
  pass

class Procedure (PlsqlCode):
  pass

class Package (PlsqlCode):
  pass

class Trigger (PlsqlCode):
  pass

class Type (PlsqlCode):
  pass

class Schema (object):

  share_namespace = set(
        Table,
        View,
        Sequence,
        Synonym,
        Procedure,
        Function,
        Package,
        Type
      )

  def __init__ (self, name):
    self.name = OracleFQN(name)

    # Namespaces
    self.shared_namespace = {}
    self.objects = {}
    self.deferred = {}


  def __repr__ (self):
    return "Schema('" + self.name.schema + "')"

  def add (self, obj):
    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)

    obj_type = type(obj)
    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    if (name in namespace) or (obj_type in share_namespace and
                              name in self.shared_namespace):
      if name in self.deferred and type(self.deferred[name]) == obj_type:
        # Not a name conflict
        pass
      else:
        raise TypeConflict(obj, namespace[name].type)
    else:
      obj.name = name
      namespace[name] = obj
      if obj_type in share_namespace:
        self.shared_namespace[name] = obj

  def find (self, name, obj_type=Table, deferred=True):
    name = OracleFQN(self.name.schema, name)

    if type in self.objects and name in self.objects[obj_type]:
      return self.objects[obj_type][name]

    if deferred:
      obj = obj_type(name)
      self.add(obj)
      self.deferred[name] = obj
      return obj


    return None

def fromDb (schema):
  def makeName (name):
    try:
      return OracleIdentifier(name)
    except OracleNameError:
      return OracleIdentifier('"' + name + '"')

  rs = db.query(""" SELECT object_name, object_type
                    FROM all_objects
                    WHERE owner = :o
                """, o=schema.name.schema)

  for obj in rs:
    objectName = makeName(obj['object_name'])

    className = obj['object_type'].capitalize()
    try:
      class_ = globals()[className]
      schema.add(class_(objectName))
    except (NameError, KeyError):
      print("{} [{}]: unexpected type".format(className, obj['object_name']))

  # Constraints handled differently
  rs = db.query(""" SELECT constraint_name, table_name
                    FROM all_constraints
                    WHERE owner = :o
                """, o=schema.name.schema)

  for con in rs:
    conName = makeName(con['constraint_name'])
    tableName = makeName(con['table_name'])


    table = schema.find(tableName)
    if not table:
      print("Constraint [{}] references nonexistent table [{}]"
        .format(constraint.name, tableName))

    constraint = Constraint(conName, table)
    schema.add(constraint)


if __name__ == '__main__':
  db = DBManager()

  rs = db.query('select * from foop')

  print(rs[0]['VALUE'])
