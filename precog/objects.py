from precog import db
from precog.diff import Diff, order_diffs
from precog.errors import *
from precog.identifier import *
from precog.log import logging
from precog.util import InsensitiveDict

class OracleObject (object):

  def __init__ (self, name, deferred=False, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name
    self.deferred = deferred
    self.props = InsensitiveDict(props)
    #for prop, value in props.items():
      #self.props[prop] = value
    self.type = type(self).__name__.upper()

  def __repr__ (self):
    return "{}({!r}, {}**{!r})".format(type(self).__name__,
        self.name, 'deferred=True, ' if self.deferred else '', self.props)

  def __str__ (self):
    return self.sql()

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    if self.name != other.name:
      return False

    if self.props != other.props:
      return False

    return True

  def __hash__ (self):
    return hash((type(self), self.name))

  def sql (self):
    return "-- Placeholder for {} {}".format(type(self).__name__, self.name)

  def satisfy (self, other):
    if self.deferred:
      self.props = other.props

      self.deferred = False

  def diff (self, other):
    """
    Calculate differences between self, which is the desired definition, and
    other, which is the current database state.
    """
    if self != other:
      logging.debug('OracleObject: self != other')
      return [Diff(self.sql(), self.dependencies(), self)]

    return []

  def diff_subobjects (self, target_objs, current_objs):
    diffs = []

    if not isinstance(target_objs, dict):
      target_objs = {obj.name: obj for obj in target_objs}
    if not isinstance(current_objs, dict):
      current_objs = {obj.name: obj for obj in current_objs}

    logging.debug("target_objs = {}".format(target_objs))
    logging.debug("current_objs = {}".format(current_objs))

    target_obj_names = set(target_objs)
    current_obj_names = set(current_objs)

    addobjs = target_obj_names - current_obj_names
    dropobjs = current_obj_names - target_obj_names

    logging.debug("addobjs = {}".format(addobjs))
    logging.debug("dropobjs = {}".format(dropobjs))

    if addobjs:
      diffs.extend(
          self.add_subobjects(target_objs[addobj] for addobj in addobjs))
    if dropobjs:
      diffs.extend(
          self.drop_subobjects(current_objs[dropobj] for dropobj in dropobjs))

    for obj_diffs in (target_obj.diff(current_objs[target_obj.name])
        for target_obj in target_objs.values()
        if target_obj.name in current_objs):
      diffs.extend(obj_diffs)

    return diffs

  def dependencies (self):
    return set()

  @classmethod
  def from_db (class_, name):
    logging.warn("Unimplemented from_db for {}".format(class_.__name__))
    return class_(name, deferred=True)

class HasColumns (object):
  """ Mixin for objects that have the columns property """

  def __init__ (self, name, columns=set(), **props):
    super().__init__(name, **props)

    self.columns = columns

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycols = {c.name: c for c in self.columns}
    othercols = {c.name: c for c in other.columns}

    return mycols == othercols

  @property
  def columns (self):
    return self._columns

  @columns.setter
  def columns (self, value):
    if not isinstance(value, set):
      raise TypeError("expected set: {}".format(value))
    self._columns = value

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.columns = other.columns

  def dependencies (self):
    return super().dependencies() | self.columns

class HasTable (object):
  """ Mixin for objects that have the table property """

  def __init__ (self, name, table=None, **props):
    super().__init__(name, **props)

    self.table = table

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False
    return self.table == other.table

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.table = other.table

  def dependencies (self):
    return super().dependencies() | {self.table}


class Table (HasColumns, OracleObject):

  def __init__ (self, name, indexes=set(), **props):
    super().__init__(name, **props)
    self.indexes = indexes

  @HasColumns.columns.setter
  def columns (self, value):
    if not isinstance(value, set):
      raise TypeError("expected set: {}".format(value))
    for column in value:
      column.table = self

    self._columns = value

  @property
  def indexes (self):
    return self._indexes

  @indexes.setter
  def indexes (self, value):
    for index in value:
      index.table = self

    self._indexes = value

  def __repr__ (self):
    return ("Table('" + self.name.obj + "', columns={" +
        ', '.join(repr(c) for c in self.columns) + '}' +
        (', indexes={' + ', '.join(repr(i) for i in self.indexes) + '}'
          if self.indexes else '') +
        ')')

  def dependencies (self):
    # a Table doesn't depend on its columns
    return set()

  def sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE TABLE {} ( {} ){}".format(name,
        ', '.join(c.sql() for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  def add_subobjects (self, columns):
    return [Diff("ALTER TABLE {} ADD ( {} )".format(self.name, column.sql()),
      self, column) for column in columns]

  def drop_subobjects (self, columns):
    return [Diff("ALTER TABLE {} DROP ( {} )".format(
      self.name, column.name.part), {self, column}) for column in columns]

  def diff (self, other):
    diffs = []

    if self.name.obj != other.name.obj:
      diffs.append(Diff("ALTER TABLE {} RENAME TO {}"
          .format(other.name, self.name.obj), other, self))

    if (self.props['tablespace_name'] and
        self.props['tablespace_name'] != other.props['tablespace_name']):
      diffs.append(Diff("ALTER TABLE {} MOVE TABLESPACE {}"
          .format(other.name, self.props['tablespace_name']), other, self))

      for i in other.indexes:
        diffs.append(Diff("ALTER INDEX {} REBUILD".format(i.name), i, i))

    diffs.extend(other.diff_subobjects(self.columns, other.columns))

    return diffs

  @classmethod
  def from_db (class_, name):
    rs = db.query(""" SELECT tablespace_name
                      FROM all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj)
    if not rs:
      return None
    return class_(name, columns=Column.from_db(name), **rs[0])



class Column (HasTable, OracleObject):

  def __init__ (self, name, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    super().__init__(name, **props)

    if 'data_type' in self.props:
      self.props['data_type'] = self.props['data_type'].upper()

    if 'data_default' in self.props and self.props['data_default']:
      self.props['data_default'] = self.props['data_default'].strip()

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

  def sql (self, fq=False):
    parts = []
    name = self.name if fq else self.name.part
    parts.append(name)

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
    parts.append(data_type)

    if 'data_default' in self.props:
      parts.append("DEFAULT {}".format(self.props['data_default']))

    return " ".join(parts)

  def diff (self, other):
    diffs = []

    if self.name.part != other.name.part:
      diffs.append(Diff("ALTER TABLE {} RENAME COLUMN {} TO {}"
          .format(other.table.name, other.name.part, self.name.part),
          {other.table, other}, self))

    prop_diff = InsensitiveDict((prop, other.props[prop])
        for prop, expected in self.props.items()
        if expected != other.props[prop])

    if prop_diff:
      for prop in prop_diff:
        logging.debug("Prop: {} expected: {}, found {}".format(prop,
          repr(self.props[prop]), repr(other.props[prop])))
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} )".format(
        other.table.name, self.sql()), {other.table, other}, self))

    return diffs

  @classmethod
  def from_db (class_, name):
    rs = db.query(""" SELECT column_name
                             , data_type
                             , data_length
                             , data_precision
                             , data_scale
                             , data_default
                        FROM all_tab_cols
                        WHERE owner = :o
                          AND table_name = :t
                          AND (:c IS NULL OR column_name = :c)
                    """, o=name.schema, t=name.obj, c=name.part)

    return {class_(name[1], **dict(props))
      for name, *props in (row.items() for row in rs)}


class Constraint (HasTable, OracleObject):
  pass

class Index (HasColumns, OracleObject):
  """ ALTER INDEX {} REBUILD TABLESPACE {} """

  @HasColumns.columns.setter
  def columns (self, value):
    if not isinstance(value, set):
      raise TypeError("expected set: {}".format(value))
    if value:
      tablename = next(iter(value)).name.obj

      for column in value:
        if column.name.obj != tablename:
          raise TableConflict(column, tablename)

      self._tablename = tablename

    self._columns = value

  def sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE {}INDEX {} ON {} ( {} ){}".format(
        'UNIQUE ' if self.props['uniqueness'] == 'UNIQUE' else '',
        name,
        self._tablename,
        ', '.join(c.name.part for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  @classmethod
  def from_db (class_, name):
    rs = db.query(""" SELECT tablespace_name
                      FROM all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj)
    if not rs:
      return None
    return class_(name, columns=Column.from_db(name), **rs[0])

class Sequence (OracleObject):
  pass

class Synonym (OracleObject):
  pass

class Grant (OracleObject):
  pass

class View (OracleObject): # Table??
  pass

class Lob (OracleObject):
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

class PackageBody (PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)
    self.type = 'PACKAGE BODY'

class Trigger (PlsqlCode):
  pass

class Type (PlsqlCode):
  pass

class TypeBody (PlsqlCode):

  def __init__ (self, name, **props):
    super().__init__(name, **props)
    self.type = 'TYPE BODY'

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

  def __init__ (self, name=None):
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

    obj_type = type(obj)
    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)
    logging.debug(
        "Adding {}{} {} as {}".format('deferred ' if obj.deferred else '',
          obj_type.__name__, obj.name, name))
    obj.name = name

    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    if (name in namespace) or (obj_type in self.share_namespace and
                              name in self.shared_namespace):
      if name in self.deferred and type(self.deferred[name]) == obj_type:
        # Not a name conflict
        logging.debug('Satisfying deferred object')
        deferred = namespace[name]
        deferred.satisfy(obj)
        del self.deferred[name]
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

    if not name.schema:
      name = OracleFQN(self.name.schema, name.obj, name.part)

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
      logging.debug("Diffing {}s".format(t.__name__))
      target_objs = self.objects[t] if t in self.objects else []
      current_objs = other.objects[t] if t in other.objects else []

      diffs.extend(other.diff_subobjects(target_objs, current_objs))

    return diffs

  def add_subobjects (self, objs):
    return [Diff(obj.sql(), obj.dependencies(), obj) for obj in objs]

  def drop_subobjects (self, objs):
    return [Diff("DROP {} {}".format(obj.type, obj.name), obj) for obj in objs]

  @classmethod
  def from_db (class_, schema_name=None):
    schema = class_(schema_name)

    owner = schema_name
    if not owner:
      owner = db.user

    def make_name (name):
      try:
        obj_name =  OracleIdentifier(name)
      except OracleNameError:
        obj_name = OracleIdentifier('"' + name + '"')

      return OracleFQN(owner, obj_name)

    rs = db.query(""" SELECT object_name, object_type
                      FROM all_objects
                      WHERE owner = :o
                  """, o=owner)

    for obj in rs:
      object_name = make_name(obj['object_name'])

      class_name = ''.join(word.capitalize()
          for word in obj['object_type'].split())
      try:
        class_ = globals()[class_name]
        obj = class_.from_db(object_name)
        schema.add(obj)
      except (NameError, KeyError) as e:
        print("{} [{}]: unexpected type".format(class_name, obj['object_name']))

    # Constraints handled differently
    rs = db.query(""" SELECT constraint_name, table_name
                      FROM all_constraints
                      WHERE owner = :o
                  """, o=owner)

    for con in rs:
      con_name = make_name(con['constraint_name'])
      table_name = make_name(con['table_name'])

      table = schema.find(table_name, Table)

      constraint = Constraint(con_name, table)
      schema.add(constraint)

    return schema

class Database (object):

  def __init__ (self, default_schema=None):
    self.schemas = {}
    self.parser = None

    if not default_schema:
      default_schema = db.user
    self.default_schema = default_schema

  def add (self, obj):
    if not obj:
      return

    if isinstance(obj, Schema):
      self.schemas[obj.name] = obj
      return

    schema_name = obj.name.schema
    if not schema_name:
      schema_name = db.user

    if schema_name not in self.schemas:
      self.schemas[schema_name] = Schema(schema_name)

    self.schemas[schema_name].add(obj)

  def add_file (self, filename):
    if not self.parser:
      from precog import parser
      self.parser = parser.file_parser(filename)

    self.parser.sqlplus_file(self)

  def find (self, name, obj_type=Table, deferred=True):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.default_schema, name)

    if not name.schema:
      name = OracleFQN(self.default_schema, name.obj, name.part)

    if name.schema not in self.schemas:
      if deferred:
        self.schemas[name.schema] = Schema(name.schema)
      else:
        return None

    return self.schemas[name.schema].find(name, obj_type, deferred)

  def validate (self):
    unsatisfied = [obj for schema in self.schemas.values()
        for obj in schema.deferred.values()]

    if unsatisfied:
      raise UnsatisfiedDependencyError(unsatisfied)

  def diff_to_db (self):
    self.validate()

    diffs = []
    for schema_name in self.schemas:
      logging.debug("Validating schema {}".format(schema_name))
      diffs.extend(self.schemas[schema_name].diff(Schema.from_db(schema_name)))

    if diffs:
      diffs = order_diffs(diffs)

    return diffs

  @classmethod
  def from_file (class_, filename):
    database = class_()

    database.add_file(filename)

    for schema in database.schemas.values():
      logging.debug("Schema {}".format(schema.name))
      for obj_type in schema.objects:
        logging.debug("  {}s:".format(obj_type.__name__))
        for obj_name in sorted([str(obj_name) for obj_name in
            schema.objects[obj_type]]):
          logging.debug("    {}".format(obj_name))

    return database

