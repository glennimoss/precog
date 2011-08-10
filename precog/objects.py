from precog import db
from precog.diff import Diff, order_diffs
from precog.errors import *
from precog.identifier import *
from precog.util import HasLog, InsensitiveDict

class OracleObject (HasLog):

  def __init__ (self, name, deferred=False, **props):
    super().__init__()
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name
    self.deferred = deferred
    self.props = InsensitiveDict(props)
    self.type = type(self).__name__.upper()

  def __repr__ (self, **other_props):
    if self.deferred:
      other_props['deferred'] = True

    other_props.update(self.props)
    return "{}({!r}, {})".format(type(self).__name__,
        self.name,
        ', '.join("{}={!r}".format(k, v) for k, v in other_props.items()))


  def __str__ (self):
    return self.sql()

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    if self.name != other.name:
      return False

    common_props = self.props.keys() & other.props.keys()
    for prop_name in common_props:
      if self.props[prop_name] != other.props[prop_name]:
        return False

    return True

  def __hash__ (self):
    return hash((type(self), self.name))

  def sql (self, fq=None):
    type_name = ''
    if self.deferred:
      type_name = 'deferred '
    elif hasattr(self, '_sql'):
      if fq is None:
        return self._sql()
      else:
        return self._sql(fq)

    type_name += type(self).__name__
    return "-- Placeholder for {} {}".format(type_name, self.name)

  def create (self):
    return Diff(self.sql(), self.dependencies(), self)

  def drop (self):
    return Diff("DROP {} {}".format(self.type, self.name), self)

  def satisfy (self, other):
    if self.deferred:
      self.props = other.props

      self.deferred = False

  def diff (self, other):
    """
    Calculate differences between self, which is the desired definition, and
    other, which is the current database state.
    """

    if other.deferred:
      self.log.warn(
          "Comparing {!r} to deferred object {!r}".format(self, other))
    if self != other:
      return [Diff(self.sql(), self.dependencies(), self)]

    return []

  def diff_subobjects (self, target_objs, current_objs):
    diffs = []

    if not isinstance(target_objs, dict):
      target_objs = {obj.name: obj for obj in target_objs}
    if not isinstance(current_objs, dict):
      current_objs = {obj.name: obj for obj in current_objs}

    self.log.debug("target_objs = {}".format(target_objs))
    self.log.debug("current_objs = {}".format(current_objs))

    target_obj_names = set(target_objs)
    current_obj_names = set(current_objs)

    addobjs = target_obj_names - current_obj_names
    dropobjs = current_obj_names - target_obj_names

    self.log.debug("addobjs = {}".format(addobjs))
    self.log.debug("dropobjs = {}".format(dropobjs))

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

  warned = False
  @classmethod
  def from_db (class_, name):
    if not class_.warned:
      HasLog.log_for(class_).warn(
          "Unimplemented from_db for {}".format(class_.__name__))
      class_.warned = True
    return class_(name, deferred=True)

class HasColumns (object):
  """ Mixin for objects that have the columns property """

  def __init__ (self, name, columns=[], **props):
    super().__init__(name, **props)

    self.columns = columns

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycols = {c.name: c for c in self.columns}
    othercols = {c.name: c for c in other.columns}

    return mycols == othercols

  def __repr__ (self, **other_props):
    other_props['columns'] = self.columns
    return super().__repr__(**other_props)

  @property
  def columns (self):
    return self._columns

  @columns.setter
  def columns (self, value):
    if not isinstance(value, list):
      raise TypeError("Expected list: {!r}".format(value))
    self._columns = value

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.columns = other.columns

  def dependencies (self):
    return super().dependencies() | set(self.columns)

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

  @property
  def table (self):
    return self._table

  @table.setter
  def table (self, value):
    if value:
      if not isinstance(value, Table):
        raise TypeError("Expected Table: {!r}".format(value))
      self._table = value

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
    HasColumns.columns.__set__(self, value)
    for column in value:
      column.table = self

  @property
  def indexes (self):
    return self._indexes

  @indexes.setter
  def indexes (self, value):
    for index in value:
      index.table = self

    self._indexes = value

  def __repr__ (self):
    return super().__repr__(indexes=self.indexes)
    #return ("Table('" + self.name.obj + "', columns=[" +
        #', '.join(repr(c) for c in self.columns) + ']' +
        #(', indexes={' + ', '.join(repr(i) for i in self.indexes) + '}'
          #if self.indexes else '') +
        #')')

  def dependencies (self):
    # a Table doesn't depend on its columns
    return set()

  def _sql (self, fq=True):
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
                  """, o=name.schema, t=name.obj,
                  oracle_names=['tablespace_name'])
    if not rs:
      return None
    return class_(name, columns=Column.from_db(name), **rs[0])



class Column (HasTable, OracleObject):

  def __init__ (self, name, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    super().__init__(name, **props)

    if self.props['data_type']:
      try:
        self.props['data_type'] = OracleIdentifier(self.props['data_type'])
      except ReservedNameError:
        self.props['data_type'] = self.props['data_type'].upper()

    if self.props['data_default']:
      self.props['data_default'] = self.props['data_default'].strip()

  @HasTable.table.setter
  def table (self, value):
    if value:
      HasTable.table.__set__(self, value)
      self.name = OracleFQN(value.name.schema, value.name.obj, self.name.part)

  def _sql (self, fq=False):
    parts = []
    name = self.name if fq else self.name.part
    parts.append(str(name))

    data_type = self.props['data_type']
    if data_type in ('NUMBER', 'FLOAT'):
      if self.props['data_precision'] or self.props['data_scale']:
        precision = (self.props['data_precision']
            if self.props['data_precision'] else '*')
        scale = (",{}".format(self.props["data_scale"])
            if self.props['data_scale'] else '')
        data_type += "({}{})".format(precision, scale)
    elif self.props['data_length']:
      data_type += "({})".format(self.props['data_length'])
    parts.append(data_type)

    if self.props['data_default']:
      parts.append("DEFAULT {}".format(self.props['data_default']))

    return " ".join(parts)

  def diff (self, other):
    super().diff(other)
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
        self.log.debug("Prop: {} expected: {}, found {}".format(prop,
          repr(self.props[prop]), repr(other.props[prop])))
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} )".format(
        other.table.name, self.sql()), {other.table, other}, self))

    if (other.props['data_default'] and
        other.props['data_default'] != 'NULL' and
        not self.props['data_default']):
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} DEFAULT NULL)".format(
        other.table.name, other.name.part), {other.table, other}, self))

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
                    """, o=name.schema, t=name.obj, c=name.part,
                    oracle_names=['column_name', 'data_type'])

    return [class_(name, **dict(props))
      for (devnull, name), *props in (row.items() for row in rs)]


class Constraint (HasTable, OracleObject):
  pass

class Index (HasColumns, OracleObject):

  @HasColumns.columns.setter
  def columns (self, value):
    HasColumns.columns.__set__(self, value)
    if value:
      tablename = value[0].name.obj

      for column in value:
        if column.name.obj != tablename:
          raise TableConflict(column, tablename)

      self._tablename = tablename

  def _sql (self, fq=True):
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

  def diff (self, other):
    diffs = []

    if self != other:
      if self.name.obj != other.name.obj:
        diffs.append(Diff("ALTER INDEX {} RENAME TO {}"
            .format(other.name, self.name.obj), other, self))

      if (self.props['tablespace_name'] and
          self.props['tablespace_name'] != other.props['tablespace_name']):
        diffs.append(Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
            .format(other.name, self.props['tablespace_name']), other, self))

      drop = other.drop()
      create = self.create()
      create.dependencies.add(drop)
      diffs.append(drop)
      diffs.append(create)

    return diffs

  @classmethod
  def from_db (class_, name):
    rs = db.query(""" SELECT uniqueness
                           , tablespace_name
                           , CURSOR(SELECT table_owner
                                         , table_name
                                         , column_name
                                    FROM all_ind_columns aic
                                    WHERE aic.index_owner = ai.owner
                                      AND aic.index_name = ai.index_name
                                    ORDER BY aic.column_position
                             ) AS columns
                      FROM all_indexes ai
                      WHERE owner = :o
                        AND index_name = :t
                  """, o=name.schema, t=name.obj,
                  oracle_names=['tablespace_name', 'table_owner', 'table_name',
                    'column_name'])
    if not rs:
      return None
    *props, (devnull, columns) = rs[0].items()
    columns = [_current_database.find(OracleFQN(col['table_owner'],
      col['table_name'], col['column_name']), Column)
      for col in columns]
    return class_(name, columns=columns, **dict(props))

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
    if not name:
      name = db.user
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
    self.log.debug(
        "Adding {}{} {} as {}".format('deferred ' if obj.deferred else '',
          obj_type.__name__, obj.name, name))

    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    if (name in namespace) or (obj_type in self.share_namespace and
                              name in self.shared_namespace):
      if name in self.deferred and type(self.deferred[name]) == obj_type:
        # Not a name conflict
        self.log.debug("Satisfying deferred object {}".format(name))
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

  def find (self, name, obj_type, deferred=True):
    self.log.debug("Finding {} {!r}".format(obj_type.__name__, name))
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
      self.log.debug("Diffing {}s".format(t.__name__))
      target_objs = self.objects[t] if t in self.objects else []
      current_objs = other.objects[t] if t in other.objects else []

      diffs.extend(other.diff_subobjects(target_objs, current_objs))

    return diffs

  def add_subobjects (self, objs):
    return [obj.create() for obj in objs]

  def drop_subobjects (self, objs):
    return [obj.drop() for obj in objs]

  @classmethod
  def from_db (class_, schema=None):
    if not isinstance(schema, class_):
      schema = class_(schema)

    owner = schema.name.schema

    schema.log.info("Fetching schema {}".format(owner))

    def make_name (name):
      return OracleFQN(owner, name, from_oracle=True)

    rs = db.query(""" SELECT object_name, object_type
                      FROM all_objects
                      WHERE owner = :o
                        AND subobject_name IS NULL
                  """, o=owner)

    for obj in rs:
      schema.log.debug(
          "Fetching {} {}".format(obj['object_type'], obj['object_name']))
      object_name = make_name(obj['object_name'])

      class_name = ''.join(word.capitalize()
          for word in obj['object_type'].split())
      try:
        class_ = globals()[class_name]
        obj = class_.from_db(object_name)
        schema.add(obj)
      except (NameError, KeyError) as e:
        schema.log.warn("{} [{}]: unexpected type".format(
          class_name, obj['object_name']))
        raise

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

    schema.log.info("Fetching schema {} complete".format(owner))
    return schema

class Database (HasLog):

  def __init__ (self, default_schema=None):
    super().__init__()
    self.schemas = {}

    if not default_schema:
      default_schema = db.user
    self.default_schema = OracleIdentifier(default_schema)
    self.log.debug("Creating with default schema {}".format(default_schema))

  def add (self, obj):
    if not obj:
      return

    schema_name = obj.name.schema
    if isinstance(obj, Schema):
      self.schemas[schema_name] = obj
      return

    if not schema_name:
      schema_name = self.default_schema

    if schema_name not in self.schemas:
      self.schemas[schema_name] = Schema(schema_name)

    self.schemas[schema_name].add(obj)

  def add_file (self, filename):
    self.log.info("Parsing file {}".format(filename))
    from precog import parser
    parser.file_parser(filename).sqlplus_file(self)

  def find (self, name, obj_type, deferred=True):
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
    self.log.info('Validating referential integrity')
    unsatisfied = [obj for schema in self.schemas.values()
        for obj in schema.deferred.values()]

    if unsatisfied:
      raise UnsatisfiedDependencyError(unsatisfied)

  def diff_to_db (self, connection_string):
    global _current_database
    self.validate()

    self.log.info('Comparing database definition to current database state')

    db.connect(connection_string)

    _current_database = Database()

    diffs = []
    for schema_name in self.schemas:
      db_schema = Schema(schema_name)
      _current_database.add(db_schema)

    for schema in _current_database.schemas.values():
      Schema.from_db(schema)

    #_current_database.validate()

    for schema_name in self.schemas:
      diffs.extend(self.schemas[schema_name].diff(
        _current_database.schemas[schema_name]))

    if diffs:
      diffs = order_diffs(diffs)

    return diffs

  @classmethod
  def from_file (class_, filename, default_schema=None):
    database = class_(default_schema)

    database.add_file(filename)

    for schema in database.schemas.values():
      database.log.debug("Schema {}".format(schema.name))
      for obj_type in schema.objects:
        database.log.debug("  {}s:".format(obj_type.__name__))
        for obj_name in sorted([obj_name for obj_name in
            schema.objects[obj_type]], key=lambda n: str(n)):
          database.log.debug(
              "    {}".format(schema.objects[obj_type][obj_name].sql(True)))

    return database

_current_database = None
