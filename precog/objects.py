import logging

from precog import db
from precog.diff import Diff, order_diffs, PlsqlDiff
from precog.errors import *
from precog.identifier import *
from precog.util import (classproperty, HasLog, InsensitiveDict, ValidatingList,
    ValidationError)

def _type_to_class (type):
  class_name = ''.join(word.capitalize() for word in type.split())
  return globals()[class_name]

def _assert_type (value, type):
  if value is not None and not isinstance(value, type):
    raise TypeError("Expected {}: {!r}".format(type.__name__, value))

class _Reference (object):
  SOFT = "SOFT"
  HARD = "HARD"
  AUTODROP = "AUTODROP"

  def __init__ (self, obj, integrity=HARD):
    self.obj = obj
    self.integrity = integrity

  def __str__ (self):
    return "{} reference to {}".format(self.integrity, self.obj.pretty_name)

class OracleObject (HasLog):

  @classproperty
  def type (class_):
    return class_.__name__.upper()

  def __init__ (self, name, deferred=False, database=None, aka=None, **props):
    super().__init__()
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name
    self.deferred = deferred
    self.database = database
    self.props = InsensitiveDict(props)
    self._referenced_by = set()
    self._dependencies = set()
    self.aka = name
    if aka:
      self.aka = aka

  def __repr__ (self, **other_props):
    if self.deferred:
      other_props['deferred'] = True

    if self.aka:
      other_props['aka'] = self.aka

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

  @property
  def pretty_name (self):
    return " ".join((type(self).__name__, self.name))

  def sql (self, fq=None):
    if not self.deferred and hasattr(self, '_sql'):
      if fq is None:
        return self._sql()
      else:
        return self._sql(fq)
    return "-- Placeholder for {}{}".format(
        'deferred ' if self.deferred else '', self.pretty_name)

  def create (self):
    return Diff(self.sql(), produces=self, priority=Diff.CREATE)

  def drop (self):
    self.log.debug("{} has {}".format(self.pretty_name,
      ", ".join(str(ref) for ref in self._referenced_by)))
    drop = self._drop()
    ref_diffs = [diff
        for ref in self._referenced_by if ref.integrity is _Reference.HARD
        for diff in ref.obj.drop()]
    self.log.debug(ref_diffs)
    drop.dependencies.update(ref_diffs)
    return [drop] + ref_diffs

  def _drop (self):
    return Diff("DROP {} {}".format(self.type, self.name), #self,
        priority=Diff.DROP)

  def recreate (self, other):
    drop, *diffs = self.drop()
    diffs.extend(ref.obj.create()
        for ref in self._referenced_by
        if ref.integrity in (_Reference.AUTODROP, _Reference.HARD))
    create = self.create()
    create.dependencies.add(drop)
    diffs.append(drop)
    diffs.append(create)
    return diffs

    drops = other.drop()
    create = self.create()
    create.dependencies.add(drops[0])
    return drops + [create]

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
      return [self.create()]

    return []

  def _diff_props (self, other):
    prop_diff = InsensitiveDict((prop, expected)
        for prop, expected in self.props.items()
        if expected != other.props[prop])

    if self.log.isEnabledFor(logging.DEBUG):
      for prop in prop_diff:
        self.log.debug("Prop: {} expected: {}, found {}".format(prop,
          repr(self.props[prop]), repr(other.props[prop])))

    return prop_diff

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

  def add_subobjects (self, subobjects):
    return [obj.create() for obj in subobjects]

  def drop_subobjects (self, subobjects):
    return [diff for obj in subobjects for diff in obj.drop()]

  def depends_on (self, other, integrity=_Reference.HARD):
    ref = _Reference(other, integrity)
    self._dependencies.add(ref)
    other.referenced_by(self, integrity)

  def _build_set (self, get_objects):
    all = set()

    def recurse (_object):
      for ref in get_objects(_object):
        obj = ref.obj
        if obj not in all and obj is not self:
          all.add(obj)
          recurse(obj)

    recurse(self)
    return all

  @property
  def dependencies (self):
    return self._build_set(lambda self: self._dependencies)
    #deps = set()

    #def recurse (obj):
      #for dep in obj._dependencies:
        #if dep not in deps and dep is not self:
          #deps.add(dep)
          #recurse(dep)

    #recurse(self)
    #return deps

  def referenced_by (self, other=None, integrity=_Reference.SOFT):
    if other is None:
      return self._referenced_by

    ref = _Reference(other, integrity)
    self._referenced_by.add(ref)

  def _all_references (self):
    return self._build_set(lambda self: self._referenced_by)

  warned = False
  @classmethod
  def from_db (class_, name, into_database=None):
    if not class_.warned:
      HasLog.log_for(class_).warn(
          "Unimplemented from_db for {}".format(class_.__name__))
      class_.warned = True
    return class_(name, deferred=True, database=into_database)

class HasColumns (object):
  """ Mixin for objects that have the columns property """

  def __init__ (self, name, columns=[], column_reference=_Reference.AUTODROP,
      **props):
    self._column_reference = column_reference
    self._columns = []
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
    _assert_type(value, list)
    self._columns = value
    for column in self._columns:
      self.depends_on(column, self._column_reference)

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.columns = other.columns

class HasTable (object):
  """ Mixin for objects that have the table property """

  def __init__ (self, name, table=None, **props):
    super().__init__(name, **props)

    self.table = table

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False
    return self.table.name == other.table.name

  @property
  def table (self):
    return self._table

  @table.setter
  def table (self, value):
    if value:
      _assert_type(value, Table)
      self.depends_on(value, _Reference.AUTODROP)

    self._table = value

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.table = other.table

class Table (HasColumns, OracleObject):

  def __init__ (self, name, indexes=None, **props):
    super().__init__(name, column_reference=_Reference.SOFT, **props)
    if not indexes:
      indexes = set()
    self.indexes = indexes
    self.data = []

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

  @property
  def name (self):
    return self._name

  @name.setter
  def name (self, value):
    self._name = value
    # Reset the names of all the columns
    self.columns = self._columns

  def __repr__ (self):
    return super().__repr__(indexes=self.indexes)

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE TABLE {} ( {} ){}".format(name,
        ', '.join(c.sql() for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  def diff (self, other):
    diffs = []

    if self.name.obj != other.name.obj:
      diffs.append(Diff("ALTER TABLE {} RENAME TO {}"
          .format(other.name, self.name.obj), produces=self))

    if (self.props['tablespace_name'] and
        self.props['tablespace_name'] != other.props['tablespace_name']):
      diffs.append(Diff("ALTER TABLE {} MOVE TABLESPACE {}"
          .format(other.name, self.props['tablespace_name']), produces=self))

      for i in other.indexes:
        diffs.append(Diff("ALTER INDEX {} REBUILD".format(i.name), produces=i))

    diffs.extend(other.diff_subobjects(self.columns, other.columns))

    return diffs

  @classmethod
  def from_db (class_, name, into_database=None):
    rs = db.query(""" SELECT tablespace_name
                      FROM all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj,
                  oracle_names=['tablespace_name'])
    if not rs:
      return None
    return class_(name, database=into_database,
        columns=Column.from_db(name, into_database), **rs[0])


class Column (HasTable, OracleObject):

  def __init__ (self, name, user_type=None, leftovers=None, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    super().__init__(name, **props)

    self.user_type = user_type
    if self.user_type:
      self.props['data_type'] = self.user_type.name

    self.leftovers = leftovers

    if (self.props['data_type'] and
        not isinstance(self.props['data_type'], OracleIdentifier)):
      try:
        self.props['data_type'] = OracleIdentifier(self.props['data_type'])
      except ReservedNameError:
        self.props['data_type'] = self.props['data_type'].upper()
      except OracleNameError:
        # We'll keep it as-is. Maybe it will work, maybe it will blow up later
        pass

    if self.props['data_default']:
      self.props['data_default'] = self.props['data_default'].strip()

  def __repr__ (self):
    return super().__repr__(leftovers=self.leftovers)

  @HasTable.table.setter
  def table (self, value):
    if value:
      HasTable.table.__set__(self, value)
      self.name = OracleFQN(value.name.schema, value.name.obj, self.name.part)

  @property
  def user_type (self):
    return self._user_type

  @user_type.setter
  def user_type (self, value):
    if value:
      _assert_type(value, Type)
      self.props['data_type'] = value.name
      self.depends_on(value)
    self._user_type = value

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
    else:
      length = self.props['char_length'] or self.props['data_length']
      if length:
        data_type += "({})".format(length)
    parts.append(data_type)

    if self.props['data_default']:
      parts.append("DEFAULT {}".format(self.props['data_default']))

    if self.leftovers:
      parts.append(self.leftovers)

    return " ".join(parts)

  def create (self):
    return Diff("ALTER TABLE {} ADD ( {} )".format(self.table.name, self.sql()),
        produces=self, priority=Diff.CREATE)

  def _drop (self):
    return Diff(
        "ALTER TABLE {} DROP ( {} )".format(self.table.name, self.name.part),
        self.table, priority=Diff.DROP)

  def diff (self, other):
    super().diff(other)
    diffs = []

    if self.name.part != other.name.part:
      diffs.append(Diff("ALTER TABLE {} RENAME COLUMN {} TO {}"
          .format(other.table.name, other.name.part, self.name.part),
          produces=self))

    prop_diff = self._diff_props(other)

    if prop_diff:
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} )".format(
        other.table.name, self.sql()), produces=self))

    if (other.props['data_default'] and
        other.props['data_default'] != 'NULL' and
        not self.props['data_default']):
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} DEFAULT NULL)".format(
        other.table.name, other.name.part), produces=self))

    return diffs

  @classmethod
  def from_db (class_, name, into_database=None):
    rs = db.query(""" SELECT column_name
                           , data_type
                           , CASE WHEN data_type_owner = 'PUBLIC'
                                    OR data_type_owner LIKE '%SYS' THEN NULL
                                  ELSE data_type_owner
                             END AS data_type_owner
                           , data_length
                           , data_precision
                           , data_scale
                           , data_default
                           , char_length
                           , char_used
                        FROM all_tab_columns
                        WHERE owner = :o
                          AND table_name = :t
                          AND (:c IS NULL OR column_name = :c)
                    """, o=name.schema, t=name.obj, c=name.part,
                    oracle_names=['column_name', 'data_type_owner'])

    for row in rs:
      if row['data_type_owner']:
        row['user_type'] = into_database.find(
            OracleFQN(row['data_type_owner'], row['data_type']), Type)
        del row['data_type_owner']

    return [class_(name, database=into_database, **dict(props))
      for (devnull, name), *props in (row.items() for row in rs)]


class Constraint (HasTable, OracleObject):

  # Can't drop constraints like this
  def _drop (self):
    return None


class Index (HasColumns, OracleObject):

  @HasColumns.columns.setter
  def columns (self, value):
    if value:
      tablename = value[0].name
      tablename = OracleFQN(tablename.schema, tablename.obj)

      try:
        value = ValidatingList(
          lambda i: (i.name.schema == tablename.schema and
                     i.name.obj == tablename.obj))(value)
      except ValidationError as e:
        raise TableConflict(e.invalid, tablename) from e

      HasColumns.columns.__set__(self, value)

      self._tablename = tablename
      self.database.find(tablename, Table).indexes.add(self)


  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE {}INDEX {} ON {} ( {} ){}".format(
        'UNIQUE ' if self.props['uniqueness'] == 'UNIQUE' else '',
        name,
        self._tablename,
        # TODO: what to do with column objects
        #', '.join(c.name.part for c in self.columns),
        ', '.join(c.aka.part for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  def diff (self, other):
    diffs = []

    if self != other:
      if self.name.obj != other.name.obj:
        diffs.append(Diff("ALTER INDEX {} RENAME TO {}"
            .format(other.name, self.name.obj), produces=self))

      if (self.props['tablespace_name'] and
          self.props['tablespace_name'] != other.props['tablespace_name']):
        diffs.append(Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
            .format(other.name, self.props['tablespace_name']), produces=self))

      diffs.extend(self.recreate(other))

    return diffs

  @classmethod
  def from_db (class_, name, into_database):
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
                        AND index_name = :n
                  """, o=name.schema, n=name.obj,
                  oracle_names=['tablespace_name', 'table_owner', 'table_name',
                    'column_name'])
    if not rs:
      return None
    *props, (devnull, columns) = rs[0].items()
    columns = [into_database.find(OracleFQN(col['table_owner'],
      col['table_name'], col['column_name']), Column)
      for col in columns]
    return class_(name, database=into_database, columns=columns, **dict(props))

class Sequence (OracleObject):

  def __init__ (self, name, start_with=None, **props):
    super().__init__(name, **props)
    self.start_with = start_with

  def _sql (self, fq=True, operation='CREATE', props=None):
    name = self.name.obj
    if fq:
      name = self.name

    if not props:
      props = self.props

    parts = ["{} SEQUENCE {}".format(operation, name)]
    if self.props['increment_by']:
      parts.append("INCREMENT BY {}".format(self.props['increment_by']))
    if self.props['maxvalue']:
      parts.append("MAXVALUE {}".format(self.props['maxvalue']))
    if self.props['minvalue']:
      parts.append("MINVALUE {}".format(self.props['minvalue']))
    if self.props['cycle_flag']:
      parts.append("{}CYCLE".format(
        'NO' if self.props['cycle_flag'] == 'N' else ''))
    if self.props['cache_size']:
      parts.append("CACHE {}".format(self.props['cache_size']))
    if self.props['order_flag']:
      parts.append("{}ORDER".format(
        'NO' if self.props['order_flag'] == 'N' else ''))

    if 'CREATE' == operation and self.start_with:
      # START WITH only applies on creation, and can't be validated after.
      parts.append("START WITH {}".format(self.start_with))

    return ' '.join(parts)

  def diff (self, other):
    diffs = []

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff(self._sql(operation='ALTER', props=prop_diff),
        produces=self, priority=Diff.ALTER))

    return diffs

  @classmethod
  def from_db (class_, name, into_database=None):
    rs = db.query(""" SELECT min_value
                           , max_value
                           , increment_by
                           , cycle_flag
                           , order_flag
                           , cache_size
                      FROM all_sequences
                      WHERE sequence_owner = :o
                        AND sequence_name = :n
                  """, o=name.schema, n=name.obj)
    if not rs:
      return None
    return class_(name, database=into_database, **rs[0])

class Synonym (OracleObject):
  pass

class Grant (OracleObject):
  pass

class View (OracleObject): # Table??
  pass

class Lob (OracleObject):

  # Can't drop lobs like this
  def _drop (self):
    return None

class PlsqlCode (OracleObject):

  @staticmethod
  def new (type, name, source, **props):
    # Create object of subclass, based on the Oracle type passed in
    try:
      class_ = _type_to_class(type)
      return class_(name, source=source, **props)
    except KeyError as e:
      self.log.warn("{} [{}]: unexpected type".format(
        class_name, obj['object_name']))
      raise

  def __init__ (self, name, source=None, **props):
    props['source'] = source
    super().__init__(name, **props)

  def _sql (self, fq=True):
    return "CREATE OR REPLACE {}".format(self.props['source'])

  def create (self):
    return PlsqlDiff(self.sql(), produces=self, priority=Diff.CREATE,
        terminator='\n/')

  def diff (self, other):
    diffs = super().diff(other)

    if not diffs:
      errors = other.errors()
      if errors:
        self.log.info("Suggest reapplying {}".format(self.pretty_name))
        diffs.append(self.create())

    return diffs

  def errors (self):
    rs= db.query(""" SELECT line
                           , position
                           , text
                           , attribute
                      FROM all_errors
                      WHERE owner = :o
                        AND name = :n
                        AND type = :t
                      ORDER BY sequence
                  """, o=self.name.schema, n=self.name.obj, t=self.type)
    errors = [PlsqlSyntaxError(self, row) for row in rs]
    err_num = sum(1 for e in errors if e.error['attribute'] == 'ERROR')
    warn_num = len(errors) - err_num

    log = False
    if err_num:
      log = self.log.error
    elif warn_num:
      log = self.log.warn

    if log:
      log("{} has {} errors and {} warnings".format(
        self.pretty_name, err_num, warn_num))

      for err in errors:
        if err.error['attribute'] == 'ERROR':
          err_log = self.log.error
        elif err.error['attribute'] == 'WARNING':
          err_log = self.log.warn
        else:
          self.log.debug(
              "Unknown all_errors.attribute: {}".format(row['attribute']))
        err_log(err)

    return errors

  @classmethod
  def from_db (class_, name, into_database=None):
    rs = db.query(""" SELECT text
                      FROM all_source
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

  def __init__ (self, name, header=None, **props):
    super().__init__(name, **props)
    self.header = header

  @property
  def header (self):
    return self._header

  @header.setter
  def header (self, value):
    if value:
      _assert_type(value, PlsqlHeader)
      self.depends_on(value, _Reference.AUTODROP)

    self._header = value

#######################################
# PL/SQL Code Objects
#######################################
class Function (PlsqlCode):
  pass

class Procedure (PlsqlCode):
  pass

class Package (PlsqlHeader):
  pass

class PackageBody (PlsqlBody):
  @classproperty
  def type (class_):
    return 'PACKAGE BODY'

class Trigger (PlsqlCode):
  pass

class Type (PlsqlHeader):

  def diff (self, other):
    if self != other:
      return self.recreate(other)
    else:
      return super().diff(other)


class TypeBody (PlsqlBody):
  @classproperty
  def type (class_):
    return 'TYPE BODY'

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

  def __init__ (self, name=None, **props):
    if not name:
      name = db.user
    super().__init__(OracleFQN(name), **props)

    # Namespaces
    self.shared_namespace = {}
    self.objects = {}
    self.deferred = {}

  def add (self, obj):
    if not obj:
      return

    obj_type = type(obj)
    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)
    self.log.debug(
        "Adding {}{} as {}".format('deferred ' if obj.deferred else '',
          obj.pretty_name, name))

    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    if (name, obj_type) in self.deferred:
      # Not a name conflict
      self.log.debug("Satisfying deferred object {}".format(name))
      deferred = self.deferred[(name, obj_type)]
      deferred.satisfy(obj)
      del self.deferred[(name, obj_type)]
    else:
      if name in namespace:
        raise SchemaConflict(obj, namespace[name])
      elif obj_type in self.share_namespace and name in self.shared_namespace:
        raise SchemaConflict(obj, self.shared_namespace[name])
      else:
        obj.name = name
        obj.database = self.database
        namespace[name] = obj
        if obj_type in self.share_namespace:
          self.shared_namespace[name] = obj

    if Table == obj_type:
      for col in obj.columns:
        self.add(col)

  def find (self, name, obj_type, deferred=True):
    self.log.debug("Finding {} {}".format(obj_type.__name__, name))
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.name.schema, name)

    if not name.schema:
      name = OracleFQN(self.name.schema, name.obj, name.part)

    if name.part and name.part.parts:
      # TODO: how to look up multiple parts...
      lookup_by = OracleFQN(name.schema, name.obj, name.part.parts[0])
      obj = self.find(lookup_by, obj_type, deferred)
      obj.aka = name
      return obj

    if obj_type in self.objects and name in self.objects[obj_type]:
      return self.objects[obj_type][name]

    if deferred:
      obj = obj_type(name, deferred=True)
      self.add(obj)
      self.deferred[(name, obj_type)] = obj
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

  @classmethod
  def from_db (class_, schema=None, into_database=None):
    if not isinstance(schema, class_):
      schema = class_(schema, database=into_database)

    owner = schema.name.schema

    schema.log.info("Fetching schema {}...".format(owner))

    def make_name (name):
      return OracleFQN(owner, name, from_oracle=True)

    rs = db.query(""" SELECT object_name, object_type
                      FROM all_objects
                      WHERE owner = :o
                        AND subobject_name IS NULL
                  """, o=owner)

    for obj in rs:
      if obj['object_name'].startswith('SYS_'):
        schema.log.debug("Ignoring system object {}".format(obj['object_name']))
        continue

      schema.log.debug(
          "Fetching {} {}".format(obj['object_type'], obj['object_name']))
      object_name = make_name(obj['object_name'])

      try:
        class_ = _type_to_class(obj['object_type'])
        obj = class_.from_db(object_name, into_database=schema.database)
        schema.add(obj)
      except KeyError as e:
        schema.log.warn("{} [{}]: unexpected type".format(
          obj['object_type'], obj['object_name']))
        #raise

    # Constraints handled differently
    # in fact, probably not like this
    #rs = db.query(""" SELECT constraint_name, table_name
                      #FROM all_constraints
                      #WHERE owner = :o
                  #""", o=owner)

    #for con in rs:
      #con_name = make_name(con['constraint_name'])
      #table_name = make_name(con['table_name'])

      #table = schema.find(table_name, Table)

      #constraint = Constraint(con_name, table)
      #schema.add(constraint)

    schema.log.info("Fetching schema {} complete".format(owner))
    return schema

class Database (HasLog):

  def __init__ (self, default_schema=None):
    super().__init__()
    if not default_schema:
      default_schema = db.user
    self.default_schema = OracleIdentifier(default_schema)
    self.log.debug("Creating with default schema {}".format(default_schema))

    self.schemas = {}
    self.add(Schema(default_schema, database=self))

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
      self.schemas[schema_name] = Schema(schema_name, database=self)

    self.schemas[schema_name].add(obj)

  def add_file (self, filename):
    from precog import parser
    sql_parser = parser.file_parser(filename)
    sql_parser.sqlplus_file(self)
    num_errors = sql_parser.getNumberOfSyntaxErrors()
    if num_errors:
      # we don't want to compare to the database when our spec is incomplete
      raise ParseError(num_errors)

  def find (self, name, obj_type, deferred=True):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.default_schema, name)

    if not name.schema:
      name = OracleFQN(self.default_schema, name.obj, name.part)

    if name.schema not in self.schemas:
      if deferred:
        self.schemas[name.schema] = Schema(name.schema, database=self)
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
    self.validate()

    self.log.info('Comparing database definition to current database state')

    db.connect(connection_string)

    oracle_database = Database()

    diffs = []
    for schema_name in self.schemas:
      db_schema = Schema(schema_name, database=oracle_database)
      oracle_database.add(db_schema)

    for schema in oracle_database.schemas.values():
      Schema.from_db(schema)

    #oracle_database.validate()

    for schema_name in self.schemas:
      diffs.extend(self.schemas[schema_name].diff(
        oracle_database.schemas[schema_name]))

    if diffs:
      diffs = order_diffs(diffs)

    return diffs

  @classmethod
  def dump_schema (class_, connection_string, schema_name):
    db.connect(connection_string)

    oracle_database = Database()

    diffs = []
    db_schema = Schema(schema_name, database=oracle_database)
    oracle_database.add(db_schema)

    Schema.from_db(db_schema)

    diffs = db_schema.diff(Schema(schema_name))

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
