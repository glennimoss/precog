from precog import db
from precog.errors import *
from precog.identifier import *
from precog.util import InsensitiveDict

class OracleObject (object):

  def __init__ (self, name, deferred=False, **kvargs):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name
    self.deferred = deferred
    self.props = InsensitiveDict()
    for prop, value in kvargs.items():
      self.props[prop] = value
    self.type = type(self).__name__.upper()

  def __str__ (self):
    return self.sql()

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    if self.name != other.name:
      return False

    return True

  def diff (self, other):
    if self != other:
      return [self.sql()]

    return []

  def diffSubobjects (self, target_objs, current_objs):
    diffs = []

    if not isinstance(target_objs, dict):
      target_objs = {obj.name: obj for obj in target_objs}
    if not isinstance(current_objs, dict):
      current_objs = {obj.name: obj for obj in current_objs}

    target_obj_names = set(target_objs)
    current_obj_names = set(current_objs)

    addobjs = target_obj_names - current_obj_names
    dropobjs = current_obj_names - target_obj_names

    if addobjs:
      diffs.extend(
          self.addSubobjects(target_objs[addobj] for addobj in addobjs))
    if dropobjs:
      diffs.extend(
          self.dropSubobjects(current_objs[dropobj] for dropobj in dropobjs))

    for objDiffs in (target_obj.diff(current_objs[target_obj.name])
        for target_obj in target_objs.values()
        if target_obj.name in current_objs):
      diffs.extend(objDiffs)

    return diffs


  @classmethod
  def fromDb (class_, name):
    return class_(name, deferred=True)

class Table (OracleObject):

  def __init__ (self, name, columns=[], indexes=[], **kvargs):
    super().__init__(name, **kvargs)
    self.columns = []
    self.indexes = []
    for c in columns:
      c.table = self
      self.columns.append(c)
    for i in indexes:
      i.table = self
      self.indexes.append(i)

  def __repr__ (self):
    return ("Table('" + self.name.obj + "', [" +
        ', '.join(repr(c) for c in self.columns) + ']' +
        (', indexes=[' + ', '.join(repr(i) for i in self.indexes) + ']'
          if self.indexes else '') +
        ')')

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycols = {c.name: c for c in self.columns}
    othercols = {c.name: c for c in other.columns}

    return mycols == othercols


  def sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE TABLE {} ( {} ){}".format(name,
        ', '.join(c.sql() for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  def addSubobjects (self, columns):
    return ["ALTER TABLE {} ADD ( {} )".format(self.name,
          ', '.join(column.sql() for column in columns))]

  def dropSubobjects (self, columns):
    return ["ALTER TABLE {} DROP ( {} )".format(self.name,
        ', '.join(column.name.part for column in columns))]

  def satisfy (self, other):
    if self.deferred:
      self.columns = other.columns

      self.deferred = False

  def diff (self, other):
    diffs = []

    if self.name.obj != other.name.obj:
      diffs.append("ALTER TABLE {} RENAME TO {}"
          .format(other.name, self.name.obj))

    if (self.props['tablespace_name'] and
        self.props['tablespace_name'] != other.props['tablespace_name']):
      diffs.append("ALTER TABLE {} MOVE TABLESPACE {}"
          .format(other.name, self.props['tablespace_name']))

      for i in other.indexes:
        diffs.append("ALTER INDEX {} REBUILD".format(i.name))

    diffs.extend(other.diffSubobjects(self.columns, other.columns))

    return diffs

  @classmethod
  def fromDb (class_, name):
    rs = db.query(""" SELECT tablespace_name
                      FROM all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj)
    if not rs:
      return None
    return class_(name, Column.fromDb(name), **rs[0])



class Column (OracleObject):

  def __init__ (self, name, **kvargs):
    table = None
    if 'table' in kvargs:
      table = kvargs['table']
      del kvargs['table']

    super().__init__(OracleFQN(part=name), **kvargs)

    if table:
      self.table = table

    if 'data_type' in self.props:
      self.props['data_type'] = self.props['data_type'].upper()

  @property
  def table (self):
    return self._table

  @table.setter
  def table (self, value):
    self._table = value
    if value:
      self.name.schema = value.name.schema
      self.name.obj = value.name.obj

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

  def satisfy (self, other):
    if self.deferred:
      self.props = other.props
      self.table = other.table

      self.deferred = False

  def sql (self, fq=False):
    name = self.name.part
    if fq:
      name = self.name
    data_type = self.props['data_type']
    if data_type in ('NUMBER', 'FLOAT'):
      if self.props['data_precision'] or self.props['data_scale']:
        precision = (self.props['data_precision']
            if self.props['data_precision'] else '*')
        scale = (",{}".format(self.props["data_scale"])
            if self.props['data_scale'] else '')
        data_type += "({}{})".format(precision, scale)
    elif 'data_length' in self.props:
      data_type += "({})".format(self.props['data_length'])

    return "{} {}".format(name, data_type)

  def diff (self, other):
    diffs = []

    if self.name.part != other.name.part:
      diffs.append("ALTER TABLE {} RENAME COLUMN {} TO {}"
          .format(other.table.name, other.name.part, self.name.part))

    propDiff = InsensitiveDict((prop, other.props[prop])
        for prop, expected in self.props.items()
        if expected != other.props[prop])

    if propDiff:
      diffs.append("ALTER TABLE {} MODIFY ( {} )".format(
        other.table.name, self.sql()))

    return diffs

  @classmethod
  def fromDb (class_, name):
    rs = db.query(""" SELECT column_name
                             , data_type
                             , data_length
                             , data_precision
                             , data_scale
                        FROM all_tab_cols
                        WHERE owner = :o
                          AND table_name = :t
                          AND (:c IS NULL OR column_name = :c)
                    """, o=name.schema, t=name.obj, c=name.part)

    return [class_(name[1], **{key.lower(): value for key, value in props})
      for name, *props in (row.items() for row in rs)]


class Constraint (OracleObject):

  def __init__ (self, name, table=None):
    super().__init__(name)
    self.table = table

class Index (OracleObject):
  """ ALTER INDEX {} REBUILD TABLESPACE {} """
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

class Schema (OracleObject):

  share_namespace = {
        Table,
        View,
        Sequence,
        Synonym,
        Procedure,
        Function,
        Package,
        Type
      }

  def __init__ (self, name):
    super().__init__(OracleFQN(name))

    # Namespaces
    self.shared_namespace = {}
    self.objects = {}
    self.deferred = {}


  def __repr__ (self):
    return "Schema('" + self.name.schema + "')"

  def add (self, obj):
    if not obj:
      return

    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)

    obj_type = type(obj)
    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    if (name in namespace) or (obj_type in self.share_namespace and
                              name in self.shared_namespace):
      if name in self.deferred and type(self.deferred[name]) == obj_type:
        # Not a name conflict
        deferred = namespace[name]
        deferred.satisfy(obj)
      else:
        raise SchemaConflict(obj, namespace[name])
    else:
      obj.name = name
      namespace[name] = obj
      if obj_type in self.share_namespace:
        self.shared_namespace[name] = obj

    if Table == obj_type:
      for col in obj.columns:
        self.add(col)

  def find (self, name, obj_type=Table, deferred=True):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.name.schema, name)

    if obj_type in self.objects and name in self.objects[obj_type]:
      return self.objects[obj_type][name]

    if deferred:
      obj = obj_type(name, deferred=True)
      self.add(obj)
      self.deferred[name] = obj
      return obj


    return None

  def diff (self, other):
    diffs = []

    types = set(self.objects).union(other.objects) - {Column}
    for t in types:
      target_objs = self.objects[t] if t in self.objects else []
      current_objs = other.objects[t] if t in other.objects else []

      diffs.extend(other.diffSubobjects(target_objs, current_objs))

    return diffs

  def addSubobjects (self, objs):
    return [obj.sql() for obj in objs]

  def dropSubobjects (self, objs):
    return ["DROP {} {}".format(obj.type, obj.name) for obj in objs]

  @classmethod
  def fromDb (class_, schemaName):
    schema = class_(schemaName)

    def makeName (name):
      try:
        objName =  OracleIdentifier(name)
      except OracleNameError:
        objName = OracleIdentifier('"' + name + '"')

      return OracleFQN(schema.name.schema, objName)

    rs = db.query(""" SELECT object_name, object_type
                      FROM all_objects
                      WHERE owner = :o
                  """, o=schema.name.schema)

    for obj in rs:
      objectName = makeName(obj['object_name'])

      className = obj['object_type'].capitalize()
      try:
        class_ = globals()[className]
        obj = class_.fromDb(objectName)
        schema.add(obj)
      except (NameError, KeyError) as e:
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

    return schema

