import logging, re, collections

from precog import db
from precog.diff import Commit, Diff, order_diffs, PlsqlDiff, Reference
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

class OracleObject (HasLog):

  @classproperty
  def type (class_):
    return class_.pretty_type.upper()

  @classproperty
  def pretty_type (class_):
    return " ".join(re.sub('([A-Z])', r' \1', class_.__name__).split())

  def __init__ (self, name, deferred=False, database=None, aka=None,
                reinit=False, **props):
    if not reinit:
      super().__init__()
      self.deferred = deferred
      self.database = database
      self.props = InsensitiveDict(props)
      self._referenced_by = set()
      self._dependencies = set()
      self.aka = aka

    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name

  def __repr__ (self, **other_props):
    if self.deferred:
      other_props['deferred'] = True

    if self._aka:
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
  def aka (self):
    if self._aka:
      return self._aka
    else:
      return self.name

  @aka.setter
  def aka (self, value):
    self._aka = value

  @property
  def pretty_name (self):
    return " ".join((self.pretty_type, self.name, str(id(self))))

  def sql (self, fq=None):
    if not self.deferred:
      return self._sql(**{'fq': val for val in (fq,) if val is not None})
    return OracleObject._sql(self, fq)

  def _sql (self, fq=True):
    return "-- Placeholder for {}{}".format(
        'deferred ' if self.deferred else '', self.pretty_name)

  def create (self):
    return [Diff(self.sql(), produces=self, priority=Diff.CREATE)]

  def drop (self):
    self.log.debug("Dropping {}".format(self.pretty_name))
    for ref in self._referenced_by:
      self.log.debug(ref)
    drop = self._drop()
    ref_diffs = [diff
                 for ref in self._referenced_by
                   if ref.integrity is Reference.HARD
                 for diff in ref.from_.drop()]
    drop.add_dependencies(ref_diffs)
    return [drop] + ref_diffs

  def _drop (self):
    return Diff("DROP {} {}".format(self.type, self.name), self,
                priority=Diff.DROP)

  def recreate (self, other):
    """
    Recreate this object from scratch. Usually means a drop and a create.
    """
    drop, *diffs = other.drop()
    diffs.extend(diff
        for ref in self._referenced_by
          if ref.integrity in (Reference.AUTODROP, Reference.HARD)
        for diff in ref.from_.create())
    creates = self.create()
    for diff in creates:
      diff.add_dependencies(drop)
    diffs.append(drop)
    diffs.extend(creates)
    return diffs

  def rebuild (self):
    """
    Try to rebuild this object non-destructively. Used when the object is in an
    invalid state. If it can't be done non-destructively, it will attempt to
    recreate the object.
    """
    return self.recreate(self)

  def rename (self, other):
    return Diff("ALTER {} {} RENAME TO {}"
        .format(self.type, other.name, self.name.obj), produces=self)

  def satisfy (self, other):
    if self.deferred:
      self.props = other.props

      self.deferred = False

  def diff (self, other, create=True):
    """
    Calculate differences between self, which is the desired definition, and
    other, which is the current database state.
    """

    if other.deferred:
      self.log.warn(
          "Comparing {!r} to deferred object {!r}".format(self, other))
    if self != other:
      if create:
        return self.create()
      elif self.name.obj != other.name.obj:
        return [self.rename(other)]
    else:
      if other.props['status'] and other.props['status'] != 'VALID':
        self.log.debug("{} has status {}".format(other.pretty_name,
          other.props['status']))
        return other.rebuild()

    return []

  def _diff_props (self, other):
    prop_diff = InsensitiveDict((prop, expected)
        for prop, expected in self.props.items()
        if expected != other.props[prop])

    if self.log.isEnabledFor(logging.DEBUG):
      for prop in prop_diff:
        self.log.debug("{}['{}']: expected {}, found {}".format(
          self.pretty_name, prop, repr(self.props[prop]),
          repr(other.props[prop])))

    return prop_diff

  def diff_subobjects (self, other, get_objects, label=lambda x: x.name):
    self.log.debug("Diffing definition {} to live {}".format(self.pretty_name,
      other.pretty_name))
    diffs = []

    target_objs = get_objects(self)
    current_objs = get_objects(other)

    if not isinstance(target_objs, dict):
      target_objs = {label(obj): obj for obj in target_objs}
    if not isinstance(current_objs, dict):
      current_objs = {label(obj): obj for obj in current_objs}

    target_obj_names = set(target_objs)
    current_obj_names = set(current_objs)

    self.log.debug("target_obj_names = {}".format(target_obj_names))
    self.log.debug("current_obj_names = {}".format(current_obj_names))

    addobjs = target_obj_names - current_obj_names
    dropobjs = current_obj_names - target_obj_names

    pretty_type = ((target_objs and
                    type(next(iter(target_objs.values()))).pretty_type) or
                   (current_objs and
                    type(next(iter(current_objs.values()))).pretty_type) or
                   'Object')
    self.log.debug("  Adding {} {}s: {}".format(len(addobjs), pretty_type,
      ", ".join(target_objs[obj].pretty_name for obj in addobjs)))
    self.log.debug("  Dropping {} {}s: {}".format(len(dropobjs), pretty_type,
      ", ".join(current_objs[obj].pretty_name for obj in dropobjs)))

    if addobjs:
      diffs.extend(
          other.add_subobjects(target_objs[addobj] for addobj in addobjs))
    if dropobjs:
      diffs.extend(
          other.drop_subobjects(current_objs[dropobj] for dropobj in dropobjs))

    modify_diffs = [diff
        for target_obj in target_objs.values()
          if target_obj.name in current_objs
        for diff in target_obj.diff(current_objs[target_obj.name])]
    self.log.debug("  {} modifications for {}s".format(
      len(modify_diffs), pretty_type))
    diffs.extend(modify_diffs)

    return diffs

  def add_subobjects (self, subobjects):
    return [diff for obj in subobjects for diff in obj.create()]

  def drop_subobjects (self, subobjects):
    return [diff for obj in subobjects for diff in obj.drop()]

  def _depends_on (self, other, prop_name, integrity=Reference.HARD):
    old_dep = None
    if hasattr(self, prop_name):
      old_dep = getattr(self, prop_name)

    if old_dep != other:
      if old_dep:
        self._drop_dependency(old_dep)
      if other:
        self._set_dependency(other, integrity)

    setattr(self, prop_name, other)

  def _set_dependency (self, dep, integrity=Reference.HARD):
    if isinstance(dep, OracleObject):
      dep = [dep]
    self.log.debug("{} depends {} on [{}]".format(self.pretty_name, integrity,
      ", ".join(obj.pretty_name for obj in dep)))
    for obj in dep:
      ref = Reference(self, obj, integrity)
      self._dependencies.add(ref)
      #obj.referenced_by(self, integrity)
      obj._referenced_by.add(ref)

  def _drop_dependency (self, old_deps):
    if isinstance(old_deps, OracleObject):
      old_deps = [old_deps]
    self.log.debug("{} no longer depends on [{}]".format(self.pretty_name,
      ", ".join(old_dep.pretty_name for old_dep in old_deps)))
    remove_deps = set()
    for dep in self._dependencies:
      if dep.to in old_deps:
        remove_deps.add(dep)
        remove_refs = set()
        for ref in dep.to._referenced_by:
          if ref.from_ == self:
            remove_refs.add(ref)
        dep.to._referenced_by.difference_update(remove_refs)
    self._dependencies.difference_update(remove_deps)

  def _build_set (self, get_objects, get_ref, test=lambda x: True):
    all = set()

    def recurse (_object):
      for ref in get_objects(_object):
        if test(ref):
          obj = get_ref(ref)
          if obj not in all and obj != self:
            all.add(obj)
            recurse(obj)

    recurse(self)
    return all

  def become (self, other_type):
    name = self.name
    self.__class__ = other_type
    self.__init__(name, reinit=True)

  @property
  def dependencies (self):
    return self._build_set(lambda self: self._dependencies, lambda ref: ref.to)

  def dependencies_with(self, integrity):
    ret =  self._build_set(lambda self: self._dependencies, lambda ref: ref.to,
                           lambda ref: ref.integrity == integrity)
    return ret

  warned = False
  @classmethod
  def from_db (class_, name, into_database):
    if not class_.warned:
      HasLog.log_for(class_).warn(
          "Unimplemented from_db for {}".format(class_.__name__))
      class_.warned = True
    return class_(name, deferred=True, database=into_database)

class HasColumns (object):
  """ Mixin for objects that have the columns property """

  def __init__ (self, name, columns=[], column_reference=Reference.AUTODROP,
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
    if self._column_reference:
      self._depends_on(value, '_columns', self._column_reference)
    else:
      self._columns = value

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.columns = other.columns

class HasTable (object):
  """ Mixin for objects that have the table property """

  def __init__ (self, name, table=None, **props):
    super().__init__(name, **props)

    self._table = None
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
    _assert_type(value, Table)
    self._depends_on(value, '_table', Reference.AUTODROP)

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.table = other.table

class Table (HasColumns, OracleObject):

  def __init__ (self, name, indexes=None, **props):
    super().__init__(name, column_reference=None, **props)
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
    return super().__repr__(indexes=self.indexes, data=self.data)

  def add_data (self, columns, values):
    self.data.append(Data(self, columns, values))

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    return "CREATE TABLE {} ( {} ){}".format(name,
        ', '.join(c.sql() for c in self.columns),
        " TABLESPACE {}".format(self.props['tablespace_name'])
          if self.props['tablespace_name'] else '')

  def create (self):
    diffs = super().create()
    inserts = [diff for datum in self.data for diff in datum.create()]
    if inserts:
      diffs.extend(inserts)
      diffs.append(Commit(inserts))
    return diffs

  def diff (self, other):
    diffs = super().diff(other, False)

    if (self.props['tablespace_name'] and
        self.props['tablespace_name'] != other.props['tablespace_name']):
      diffs.append(Diff("ALTER TABLE {} MOVE TABLESPACE {}"
          .format(other.name, self.props['tablespace_name']), produces=self))

      for i in other.indexes:
        diffs.append(Diff("ALTER INDEX {} REBUILD".format(i.name), produces=i))

    diffs.extend(self.diff_subobjects(other, lambda o: o.columns))

    if self.data:
      Data.from_db(other)

    inserts = self.diff_subobjects(other, lambda o: o.data, lambda o: o._comp())
    if inserts:
      diffs.extend(inserts)
      diffs.append(Commit(inserts))

    return diffs

  @property
  def dependencies (self):
    deps = OracleObject.dependencies.__get__(self)
    return deps | {dep for col in self.columns
                       for dep in col.dependencies if dep != self}

  @classmethod
  def from_db (class_, name, into_database):
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
    HasTable.table.__set__(self, value)
    if value:
      self.name = OracleFQN(value.name.schema, value.name.obj, self.name.part)

  @property
  def user_type (self):
    return self._user_type

  @user_type.setter
  def user_type (self, value):
    _assert_type(value, Type)
    self._depends_on(value, '_user_type')
    if value:
      self.props['data_type'] = value.name

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
        data_type += "({}{})".format(length,
                                     (" CHAR" if self.props['char_used'] == 'C'
                                              else " BYTE")
                                     if self.props['char_used'] else '')
    parts.append(data_type)

    if self.props['data_default']:
      parts.append("DEFAULT {}".format(self.props['data_default']))

    if self.leftovers:
      parts.append(self.leftovers)

    return " ".join(parts)

  def create (self):
    return [Diff("ALTER TABLE {} ADD ( {} )".format(
      self.table.name, self.sql()), produces=self, priority=Diff.CREATE)]

  def _drop (self):
    return Diff(
        "ALTER TABLE {} DROP ( {} )".format(self.table.name, self.name.part),
        self.table, priority=Diff.DROP)


  def rename (self, other):
    return Diff("ALTER TABLE {} RENAME COLUMN {} TO {}"
          .format(other.table.name, other.name.part, self.name.part),
          produces=self)

  def diff (self, other):
    diffs = super().diff(other, False)

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
  def from_db (class_, name, into_database):
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

class Data (HasColumns, OracleObject):

  def __init__ (self, table, columns, expressions, **props):
    super().__init__(OracleFQN(table.name.schema, table.name.obj,
      "__DATA_{}".format(len(table.data))), columns=columns, **props)

    self.table = table
    self.expressions = expressions

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    return self.table.name == other.table.name and self._comp() == other._comp()

  def __hash__ (self):
    return hash((self.table.name, self._comp()))

  def _comp (self):
    """ A tuple view for hashing, comparing, etc. """
    return tuple(sorted((col, val) for col, val in self.values().items()
                        if val is not None))

  def values (self):
    return collections.OrderedDict(zip((col.name.part for col in self.columns),
                                       self.expressions))

  def _sql (self, fq=True):
    table_name = self.table.name
    if not fq:
      table_name = table_name.obj
    values = self.values()
    return "INSERT INTO {} ({}) VALUES ({})".format(self.table.name,
      ", ".join(values.keys()), ", ".join(values.values()))

  def _drop (self):
    return Diff("DELETE FROM {} WHERE {}".format(
      self.table.name, " AND ".join(" = ".join((col, val)) if val is not None
                                    else "{} IS NULL".format(col)
                                    for col, val in self.values().items())))

  def diff (self, other):
    return []

  @staticmethod
  def escape (string):
    if isinstance(string, str):
      return "'{}'".format(string.replace("'", "''"))
    elif string is not None:
      return str(string)
    else:
      return string

  @classmethod
  def from_db (class_, table):
    rs = db.query(""" SELECT *
                      FROM {}
                  """.format(table.name))

    if rs:
      columns = [table.database.find(
        OracleFQN(table.name.schema, table.name.obj, column_name), Column)
        for column_name in rs[0]]

      for row in rs:
        table.add_data(columns, [Data.escape(col) for col in row.values()])

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

  def rebuild (self):
    return [Diff("ALTER INDEX {} REBUILD".format(self.name), produces=self)]

  def diff (self, other):
    diffs = super().diff(other, False)

    prop_diffs = self._diff_props(other)
    if len(prop_diffs) == 1 and 'tablespace_name' in self.props:
      diffs.append(Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
          .format(other.name, self.props['tablespace_name']), produces=self))
    elif len(prop_diffs):
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
    diffs = super().diff(other, False)

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff(self._sql(operation='ALTER', props=prop_diff),
        produces=self, priority=Diff.ALTER))

    return diffs

  @classmethod
  def from_db (class_, name, into_database):
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

  def __init__ (self, name, for_object=None, **props):
    super().__init__(name, **props)
    self.for_object = for_object

  @property
  def for_object (self):
    return self._for_object

  @for_object.setter
  def for_object (self, obj):
    _assert_type(obj, OracleObject)
    self._depends_on(obj, '_for_object', Reference.SOFT)
    self.props['for_object'] = obj.name

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name

    return "CREATE OR REPLACE SYNONYM {} FOR {}".format(name,
                                                        self.for_object.name)

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT table_owner
                           , table_name
                      FROM all_synonyms
                      WHERE owner = :o
                        AND synonym_name = :n
                  """, o=name.schema, n=name.obj)
    if not rs:
      return None
    rs = rs[0]
    return class_(name, into_database.find(OracleFQN(rs['table_owner'],
                                                     rs['table_name']),
                                           OracleObject),
                  database=into_database)

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
  def from_db (class_, name, into_database):
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
    _assert_type(value, PlsqlHeader)
    self._depends_on(value, '_header', Reference.AUTODROP)


#######################################
# PL/SQL Code Objects
#######################################
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

class Schema (OracleObject):

  share_namespace = {
        Table,
        View,
        Sequence,
        Synonym,
        Procedure,
        Function,
        Package,
        Type,
        OracleObject
      }

  def __init__ (self, name=None, **props):
    if not name:
      name = db.user
    super().__init__(OracleFQN(name), **props)

    # Namespaces
    self.shared_namespace = {}
    self.objects = {}
    self.deferred = {}

  def _resolve_unknown_type (self, name, obj_type):
    if obj_type is not OracleObject and (name, OracleObject) in self.deferred:
      untyped_obj = self.deferred[(name, OracleObject)]
      self.log.debug("Untyped object {} is now {}".format(
        untyped_obj.pretty_name, obj_type.pretty_type))
      # clean up OracleObject references because we don't really want them
      del self.deferred[(name, OracleObject)]
      del self.objects[OracleObject][name]
      # Pretend it was of obj_type all along
      untyped_obj.become(obj_type)
      self.objects[obj_type][name] = untyped_obj
      self.deferred[(name, obj_type)] = untyped_obj

  def add (self, obj):
    if not obj:
      return

    obj_type = type(obj)
    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)
    if obj.deferred:
      self.log.debug(
          "Adding {}{} as {}".format('deferred ' if obj.deferred else '',
            obj.pretty_name, name))

    if not obj_type in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    self._resolve_unknown_type(name, obj_type)

    if (name, obj_type) in self.deferred:
      # Not a name conflict
      deferred = self.deferred[(name, obj_type)]
      self.log.debug("Satisfying deferred {} with {}".format(
        deferred.pretty_name, obj.pretty_name))
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

    if obj_type is Table:
      for col in obj.columns:
        self.add(col)

  def find (self, name, obj_type, deferred=True):
    #self.log.debug("Finding {} {}".format(obj_type.__name__, name))
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

    # When you don't know what type you're looking up, it must be in the shared
    # namespace to return a real object. Otherwise it wil be deferred.
    if obj_type is OracleObject and name in self.shared_namespace:
      return self.shared_namespace[name]

    self._resolve_unknown_type(name, obj_type)

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

    types = (set(self.objects) | other.objects) - {Column}
    for t in types:
      diffs.extend(self.diff_subobjects(other,
        lambda o: o.objects[t] if t in o.objects else []))

    return diffs

  @classmethod
  def from_db (class_, schema=None, into_database=None):
    if not isinstance(schema, class_):
      schema = class_(schema, database=into_database)

    owner = schema.name.schema

    schema.log.info("Fetching schema {}...".format(owner))

    def make_name (name):
      return OracleFQN(owner, name, from_oracle=True)

    rs = db.query(""" SELECT object_name
                           , object_type
                           , status
                      FROM all_objects
                      WHERE owner = :o
                        AND subobject_name IS NULL
                  """, o=owner)

    for obj in rs:
      if obj['object_name'].startswith('SYS_'):
        schema.log.debug("Ignoring system object {}".format(obj['object_name']))
        continue

      #schema.log.debug(
          #"Fetching {} {}".format(obj['object_type'], obj['object_name']))
      object_name = make_name(obj['object_name'])

      try:
        class_ = _type_to_class(obj['object_type'])
        db_obj = class_.from_db(object_name, schema.database)
        db_obj.props['status'] = obj['status']
        schema.add(db_obj)
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
    #self.log.debug("Creating with default schema {}".format(default_schema))

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
