import logging, re, collections, pprint

from precog import db
from precog.diff import Commit, Diff, order_diffs, PlsqlDiff, Reference
from precog.errors import *
from precog.identifier import *
from precog.util import (classproperty, HasLog, InsensitiveDict, ValidatingList,
                         ValidationError)

class _UnexpectedTypeError (KeyError):
  pass

def _type_to_class (type):
  class_name = ''.join(word.capitalize() for word in type.split())
  try:
    return globals()[class_name]
  except KeyError:
    raise _UnexpectedTypeError()

def _assert_type (value, type):
  if value is not None:
    if not isinstance(value, type):
      raise TypeError("Expected {}: {!r}".format(type.__name__, value))

def _assert_contains_type (value, contains_type):
  if value is not None:
    bad = []
    for item in value:
      try:
        _assert_type(item, contains_type)
      except TypeError as e:
        bad.append(e)

      if bad:
        raise TypeError("In container {}: {}".format(pprint.pformat(value),
                                                     ", ".join(bad)))

def _in_props (key):
  def getter (self):
    return self.props[key]

  def setter (self, value):
    self.props[key] = value

  def deller (self):
    del self.props[key]

  return property(getter, setter, deller,
                  "Property {} backed by OracleObject.props".format(key))

class OracleObject (HasLog):

  @classproperty
  def type (class_):
    return class_.pretty_type.upper()

  @classproperty
  def pretty_type (class_):
    return re.sub('([A-Z])', r' \1', class_.__name__).strip()

  def __init__ (self, name, deferred=False, database=None, reinit=False,
                **props):
    if not reinit:
      super().__init__()
      self.deferred = deferred
      self.database = database
      self.props = InsensitiveDict(props)
      self._referenced_by = set()
      self._dependencies = set()

    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name

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

  @property
  def pretty_name (self):
    return " ".join((self.pretty_type, self.name) +
                    (
                      (str(id(self)),) if self.log.isEnabledFor(logging.DEBUG)
                      else ()
                    ))

  def sql (self, **args):
    if not self.deferred:
      return self._sql(**args)
    return OracleObject._sql(self, **{'fq': args[k] for k in args if k == 'fq'})

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
    return Diff("DROP {} {}".format(self.type, self.name.lower()), self,
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
    return Diff("ALTER {} {} RENAME TO {}".format(self.type, other.name.lower(),
                                                  self.name.obj.lower()),
                produces=self)

  def satisfy (self, other):
    if self.deferred:
      self.props = other.props

      self.deferred = False

  @property
  def subobjects (self):
    return set()

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

  @classmethod
  def from_db (class_, name, into_database):
    raise UnimplementedFeatureError(
      "Unimplemented from_db for {}".format(class_.__name__))

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
    _assert_contains_type(value, Column)
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
    self._table = None
    super().__init__(name, **props)

    self.table = table

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False
    return ((not self.table and not other.table) or
            (self.table and other.table and
             self.table.name == other.table.name))

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

class HasUserType (object):

  def __init__ (self, name, user_type=None, **props):
    super().__init__(name, **props)

    self.user_type = user_type

  _user_type = _in_props('user_type')

  @_user_type.setter
  def user_type (self, value):
    _assert_type(value, Type)
    self._depends_on(value, '_user_type')

class HasConstraints (object):

  def __init__ (self, name, constraints=None, **props):
    super().__init__(name, **props)

    if not constraints:
      constraints = set()
    self.constraints = constraints

  _constraints = _in_props('constraints')

  @_constraints.setter
  def constraints (self, value):
    _assert_type(value, set)
    _assert_contains_type(value, Constraint)
    self._constraints = value
    if value:
      self.other_constraints = {cons for cons in value
                           if not isinstance(cons, UniqueConstraint)}
      self.unique_constraints = {cons for cons in value
                                  if isinstance(cons, UniqueConstraint)}
    else:
      self.other_constraints = set()
      self.unique_constraints = set()

class Table (HasConstraints, HasColumns, OracleObject):

  def __new__ (class_, *args, **props):
    if 'table_type' in props and props['table_type']:
      class_ = ObjectTable
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, indexes=None, **props):
    super().__init__(name, column_reference=None, **props)
    if not indexes:
      indexes = set()
    self.indexes = indexes
    self.data = []

  @HasColumns.columns.setter
  def columns (self, value):
    HasColumns.columns.__set__(self, value)
    if value:
      for column in value:
        column.table = self

  @HasConstraints.constraints.setter
  def constraints (self, value):
    HasConstraints.constraints.__set__(self, value)
    if value:
      for cons in value:
        cons.table = self

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

  @property
  def subobjects (self):
    return self.constraints.union(self.columns)

  def add_data (self, columns, values):
    self.data.append(Data(self, columns, values))

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    parts = ["CREATE TABLE {}{}".format(name.lower(), self._sub_sql())]
    if self.props['tablespace_name']:
      parts.append("TABLESPACE {}"
                   .format(self.props['tablespace_name'].lower()))
    return " ".join(parts)

  def _sub_sql (self):
    parts = [col.sql() for col in self.columns
             if col.props['hidden_column'] == 'NO']
    parts.extend(cons.sql() for cons in self.other_constraints)
    return "\n  ( {}\n  )".format("\n  , ".join(parts))

  def create (self):
    diffs = super().create()
    diffs.extend(diff for cons in self.unique_constraints
                 for diff in cons.create())
    diffs.extend(diff for column in self.columns
                 for cons in column.unique_constraints
                 for diff in cons.create())
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
                        .format(other.name.lower(),
                                self.props['tablespace_name'].lower()),
                        produces=self))

      for i in other.indexes:
        diffs.append(Diff("ALTER INDEX {} REBUILD".format(i.name.lower()),
                          produces=i))

    diffs.extend(self.diff_subobjects(other, lambda o: o.columns))
    diffs.extend(self.diff_subobjects(other, lambda o: o.constraints))

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
    return (deps |
            {dep for col in self.columns
             for dep in col.dependencies if dep != self} |
            {dep for cons in self.other_constraints
             for dep in cons.dependencies if dep != self})

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT table_type
                           , CASE WHEN table_type_owner = 'PUBLIC'
                                    OR table_type_owner LIKE '%SYS' THEN NULL
                                  ELSE table_type_owner
                             END AS table_type_owner
                           , tablespace_name
                      FROM all_all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj,
                  oracle_names=['tablespace_name'])
    if not rs:
      return None
    props = rs[0]
    if props['table_type_owner']:
      props['user_type'] = into_database.find(
        OracleFQN(props['table_type_owner'], props['table_type']), Type)
      del props['table_type_owner']
    elif not props['table_type']:
      props['columns'] = Column.from_db(name, into_database)

    props['constraints'] = Constraint.from_db(name, into_database)

    return class_(name, database=into_database, **props)

class ObjectTable (HasUserType, Table):
  namespace = Table

  @classproperty
  def type (class_):
    return Table.type

  @HasUserType.user_type.setter
  def user_type (self, value):
    HasUserType.user_type.__set__(self, value)
    if value:
      self.props['table_type'] = value.name.lower()

  def _sub_sql (self):
    return " OF {}".format(self.props['table_type'])

class Column (HasConstraints, HasTable, HasUserType, OracleObject):

  def __new__ (class_, *args, **props):
    if 'virtual_column' in props and 'YES' == props['virtual_column']:
      class_ = VirtualColumn
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    super().__init__(name, **props)

    if self.props['data_default']:
      self.props['data_default'] = self.props['data_default'].strip()

  @HasTable.table.setter
  def table (self, value):
    HasTable.table.__set__(self, value)
    if value:
      self.name = OracleFQN(value.name.schema, value.name.obj, self.name.part)
    # Reset the table on constraints
    self.constraints = self._constraints

  @HasUserType.user_type.setter
  def user_type (self, value):
    HasUserType.user_type.__set__(self, value)
    if value:
      self.props['data_type'] = value.name.lower()

  @HasConstraints.constraints.setter
  def constraints (self, value):
    if value:
      not_null = set()
      for cons in value:
        if (isinstance(cons, CheckConstraint) and
            cons.generated_name and
            self.props['nullable'] == 'N' and
            cons.condition == "{} IS NOT NULL"
              .format(self.name.part.force_quoted())):
          # Get rid of the system generated constraint for NOT NULL
          not_null.add(cons)
        else:
          cons.columns = [self]
      value.difference_update(not_null)

    HasConstraints.constraints.__set__(self, value)

  @property
  def subobjects (self):
    return self.constraints

  def _sql (self, fq=False, full_def=True):
    parts = []
    name = self.name
    if self.props['qualified_col_name']:
      name = OracleFQN(name.schema, name.obj, self.props['qualified_col_name'])
    if not fq:
      name = name.part
    parts.append(name.lower())

    if full_def:
      data_type = self.props['data_type']
      if data_type in ('NUMBER', 'FLOAT'):
        if self.props['data_precision'] or self.props['data_scale']:
          precision = (self.props['data_precision']
              if self.props['data_precision'] else '*')
          scale = (",{}".format(self.props["data_scale"])
              if self.props['data_scale'] else '')
          data_type += "({}{})".format(precision, scale)
      elif not self.user_type and data_type.find('CHAR') != -1:
        length = self.props['char_length'] or self.props['data_length']
        if length:
          data_type += "({}{})".format(length,
            (" CHAR" if self.props['char_used'] == 'C' else " BYTE")
            if self.props['char_used'] else '')
      parts.append(data_type)

      if self.props['data_default']:
        parts.append("DEFAULT {}".format(self.props['data_default']))

      if self.props['nullable']:
        if 'N' == self.props['nullable']:
          parts.append('NOT')
        parts.append('NULL')

      for cons in self.other_constraints:
        parts.append(cons.sql(inline=True))

    return " ".join(parts)

  def create (self):
    diffs = [Diff("ALTER TABLE {} ADD ( {} )".format(self.table.name.lower(),
                                                     self.sql()),
                  produces=self, priority=Diff.CREATE)]
    diffs.extend(diff for cons in self.unique_constraints
                 for diff in cons.create())
    return diffs

  def _drop (self):
    return Diff("ALTER TABLE {} DROP ( {} )".format(self.table.name.lower(),
                                                    self.name.part.lower()),
                self, priority=Diff.DROP)

  def rename (self, other):
    return Diff("ALTER TABLE {} RENAME COLUMN {} TO {}"
                .format(other.table.name.lower(), other.name.part.lower(),
                        self.name.part.lower()),
                produces=self)

  def diff (self, other):
    diffs = super().diff(other, False)

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} )"
                        .format(other.table.name.lower(), self.sql()),
                        produces=self))

    if (other.props['data_default'] and
        other.props['data_default'] != 'NULL' and
        not self.props['data_default']):
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} DEFAULT NULL)"
                        .format(other.table.name.lower(),
                                other.name.part.lower()),
                        produces=self))

    diffs.extend(self.diff_subobjects(other, lambda o: o.constraints))

    return diffs

  def add_subobjects (self, subobjects):
    return [Diff("ALTER TABLE {} MODIFY ({} {})"
                 .format(self.table.name.lower(), self.name.lower(),
                         " ".join(obj.sql(inline=True) for obj in subobjects)))]

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT column_name
                           , qualified_col_name
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
                           , nullable
                           , virtual_column
                           , hidden_column
                      FROM all_tab_cols
                      WHERE owner = :o
                        AND table_name = :t
                        AND (:c IS NULL OR column_name = :c)
                      ORDER BY internal_column_id
                  """, o=name.schema, t=name.obj, c=name.part,
                  oracle_names=['column_name', 'qualified_col_name',
                                'data_type_owner', 'data_type'])

    def construct (name, props):
      props = InsensitiveDict(props)
      if props['data_type_owner']:
        props['user_type'] = into_database.find(
          OracleFQN(props['data_type_owner'], props['data_type']), Type)
        del props['data_type_owner']

      constraints = Constraint.from_db(name, into_database)

      return class_(name, constraints=constraints, database=into_database,
                    **props)

    return [construct(OracleFQN(name.schema, name.obj, col_name), props)
            for (_, col_name), *props in (row.items() for row in rs)]

class VirtualColumn (Column):
  namespace = Column

  def __init__ (self, name, expression=None, **props):
    super().__init__(name, **props)

    self.expression = expression or props['data_default']
    self.props['virtual_column'] = 'YES'

  _expression = _in_props('data_default')

  @_expression.setter
  def expression (self, value):
    self._expression = value
    deps = self._parse_expression()
    self._depends_on(deps, '_expression_identifiers')

  def _parse_expression (self):
    ids = re.findall('".+?"(?:\.".+?")*', self.expression)
    deps = set()
    for id in ids:
      parts = re.split('(?<=")\.(?=")', id)
      if len(parts) == 1:
        dep = self.database.find(OracleFQN(self.name.schema, self.name.obj,
                                           parts[0]), Column)
      else:
        # TODO: we want to be able to reference items inside a package... for
        # now, we'll limit to just the package.
        # also, We're not sure if it's a global func/procedure or a package so
        # do anonymous lookup
        dep = self.database.find(OracleFQN(*parts[:2]), OracleObject)

      deps.add(dep)
    return deps

  def _sql (self, fq=False, full_def=True):
    parts = []
    hidden = 'YES' == self.props['hidden_column']

    if not hidden:
      name = self.name if fq else self.name.part
      parts.append(name.lower())

      if full_def:
        parts.append('AS (')

    if full_def or hidden:
      parts.append(self.expression)

    if not hidden and full_def:
      parts.append(')')

    return " ".join(parts)

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
    return collections.OrderedDict(zip((col.name.part.lower()
                                        for col in self.columns),
                                       self.expressions))

  def _sql (self, fq=True):
    table_name = self.table.name
    if not fq:
      table_name = table_name.obj
    values = self.values()
    return "INSERT INTO {} ({}) VALUES ({})".format(self.table.name.lower(),
      ", ".join(values.keys()), ", ".join(values.values()))

  def _drop (self):
    return Diff("DELETE FROM {} WHERE {}".format(
      self.table.name.lower(), " AND ".join(
        " = ".join((col, val)) if val is not None else "{} IS NULL".format(col)
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
    if not table.data:
      rs = db.query(""" SELECT *
                        FROM {}
                    """.format(table.name))

      if rs:
        columns = [table.database.find(
          OracleFQN(table.name.schema, table.name.obj, column_name), Column)
          for column_name in rs[0]]

        for row in rs:
          table.add_data(columns, [Data.escape(col) for col in row.values()])

class Constraint (HasColumns, HasTable, OracleObject):

  def __init__ (self, name, is_enabled=True, **props):
    super().__init__(name, **props)
    self.is_enabled = is_enabled

  generated_name = _in_props('generated_name')

  @HasColumns.columns.setter
  def columns (self, value):
    HasColumns.columns.__set__(self, value)
    if value:
      self.table = value[0].table
    else:
      self.table = None

  def _sql (self, fq=False, inline=False):
    parts = ['CONSTRAINT']
    name = self.name if fq else self.name.obj
    parts.append(name.lower())

    parts.extend(self._sub_sql(inline))

    parts.append('ENABLE' if self.is_enabled else 'DISABLE')

    return " ".join(parts)

  def _sub_sql (self, inline):
    return ['']

  def _column_list (self):
    return "( {} )".format(", ".join(col.sql(full_def=False)
                                     for col in self.columns))

  def create (self):
    return [Diff("ALTER TABLE {} ADD {}"
                 .format(self.table.name.lower(), self.sql()),
                 produces=self, priority=Diff.CREATE)]

  def _drop (self):
    return Diff( "ALTER TABLE {} DROP CONSTRAINT {}"
                .format(self.table.name.lower(), self.name.obj.lower()),
                self, priority=Diff.DROP)

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT constraint_name
                           , constraint_type
                           , status
                           , generated
                           , CURSOR(
                               SELECT table_name
                                    , column_name
                               FROM all_cons_columns acc
                               WHERE acc.owner = ac.owner
                                 AND acc.constraint_name = ac.constraint_name
                               ORDER BY acc.position
                             ) AS columns

                           -- For check constraints
                           , search_condition

                           -- For foreign key constraints
                           , r_owner
                           , r_constraint_name
                           , delete_rule

                           -- For PK/unique constraints
                           , index_owner
                           , index_name
                      FROM all_constraints ac
                      WHERE owner = :o
                        AND table_name = :n
                  """, o=name.schema, n=name.obj,
                  oracle_names=['constraint_name', 'r_owner',
                                'r_constraint_name', 'index_owner',
                                'index_name', 'table_name', 'column_name'])

    if not rs:
      return None
    constraints = set()
    for row in rs:
      if name.part:
        # We're looking only for inlineable constraints on a specific column
        if (len(row['columns']) > 1 or
            row['columns'][0]['column_name'] != name.part):
          continue
      elif len(row['columns']) == 1:
        # Only Constraints with multiple columns are at the Table level
        continue

      constraint_name = OracleFQN(name.schema, row['constraint_name'])
      type = row['constraint_type']
      constraint_class = None
      args = [constraint_name]
      columns = None
      if len(row['columns']) > 1:
        # If there's only one column, we'll leave it up to the caller to set it
        columns = [into_database.find(OracleFQN(name.schema,
                                                col['table_name'],
                                                col['column_name']),
                                      Column)
                   for col in row['columns']]
      if type == 'C':
        args.append(row['search_condition'])
        constraint_class = CheckConstraint

      elif type in ('P', 'U'):
        args.append(type)
        args.append(into_database.find(OracleFQN(row['index_owner'],
                                                 row['index_name']), Index))
        constraint_class = UniqueConstraint

      elif type == 'R':
        args.append(into_database.find(OracleFQN(row['r_owner'],
                                                 row['r_constraint_name']),
                                       Constraint))
        args.append(row['delete_rule'])
        constraint_class = ForeignKeyConstraint
      else:
        raise UnimplementedFeatureError(
          "Constraint {} has unsupported type {}".format(constraint_name, type))

      constraints.add(constraint_class(*args,
                                       is_enabled=(row['status'] == 'ENABLED'),
                                       database=into_database,
                                       generated_name=(row['generated'] ==
                                                       'GENERATED NAME'),
                                       columns=columns))

    return constraints

class CheckConstraint (Constraint):
  namespace = Constraint

  def __init__ (self, name, condition, **props):
    super().__init__(name, **props)
    self.condition = condition

  condition = _in_props('condition')

  def _sub_sql (self, inline):
    return ['CHECK (', self.condition, ')']

class UniqueConstraint (Constraint):
  namespace = Constraint

  def __init__ (self, name, type, index, **props):
    super().__init__(name, **props)
    self.is_pk = type == 'P'
    self.index = index

  is_pk = _in_props('is_pk')

  _index = _in_props('index')

  @_index.setter
  def index (self, value):
    _assert_type(value, Index)
    self._depends_on(value, '_index', Reference.AUTODROP)

  def _sub_sql (self, inline):
    parts = ['PRIMARY KEY' if self.is_pk else 'UNIQUE']
    if not inline:
      parts.append(self._column_list())
    if self.index:
      parts.append('USING INDEX')
      parts.append(self.index.name.lower())

    return parts

  def _drop (self):
    diff = super()._drop()
    diff.sql += ' KEEP INDEX'
    return diff

class ForeignKeyConstraint (Constraint):
  namespace = Constraint

  def __init__ (self, name, fk_constraint, delete_rule, **props):
    super().__init__(name, **props)
    self.fk_constraint = fk_constraint
    self.delete_rule = delete_rule

  _fk_constraint = _in_props('fk_constraint')

  @_fk_constraint.setter
  def fk_constraint (self, value):
    _assert_type(value, UniqueConstraint)
    self._depends_on(value, '_fk_constraint')

  delete_rule = _in_props('delete_rule')

  def _sub_sql (self, inline):
    parts = []
    if not inline:
      parts.append('FOREIGN KEY')
      parts.append(self._column_list())

    parts.extend(['REFERENCES', self.fk_constraint.table.name,
                  self.fk_constraint._column_list])
    if self.delete_rule != 'NO ACTION':
      parts.append('ON DELETE')
      parts.append(self.delete_rule)

    return parts

class Index (HasColumns, HasTable, OracleObject):

  @HasTable.table.setter
  def table (self, value):
    if self.table:
      self.table.indexes.discard(self)

    HasTable.table.__set__(self, value)
    if value:
      self.table.indexes.add(self)

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

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name
    parts = ['CREATE']
    if self.props['uniqueness'] == 'UNIQUE':
      parts.append('UNIQUE')
    parts.append('INDEX')
    parts.append(name.lower())
    parts.append('ON')
    parts.append(self.table.name.lower())
    parts.append('(')
    parts.append(', '.join(c.sql(full_def=False) for c in self.columns))
    parts.append(')')
    if self.props['index_type'].endswith('/REV'):
      parts.append('REVERSE')
    if self.props['tablespace_name']:
      parts.append('TABLESPACE')
      parts.append(self.props['tablespace_name'].lower())

    return " ".join(parts)

  def rebuild (self):
    return [Diff("ALTER INDEX {} REBUILD".format(self.name.lower()),
                 produces=self)]

  def diff (self, other):
    diffs = super().diff(other, False)

    prop_diffs = self._diff_props(other)
    if len(prop_diffs) == 1 and 'tablespace_name' in self.props:
      diffs.append(Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
                        .format(other.name.lower(),
                                self.props['tablespace_name'].lower()),
                        produces=self))
    elif len(prop_diffs):
      diffs.extend(self.recreate(other))

    return diffs

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT index_type
                           , uniqueness
                           , tablespace_name
                           , table_owner
                           , table_name
                      FROM all_indexes ai
                      WHERE owner = :o
                        AND index_name = :n
                  """, o=name.schema, n=name.obj,
                  oracle_names=['tablespace_name', 'table_owner', 'table_name',
                    'column_name'])
    if not rs:
      return None
    rs = rs[0]
    if rs['index_type'].find('NORMAL') == -1:
      into_database.log.warn(
        "Index {} is of unsupported type {}".format(name, rs['index_type']))
      rs['index_type'] = 'NORMAL'
      #raise UnimplementedFeatureError(
      #  "Index {} is of unsupported type {}".format(name, rs['index_type']))
    *props, (_, table_owner), (_, table_name) = rs.items()
    table = into_database.find(OracleFQN(table_owner, table_name), Table)

    # *Sigh*, we can't query the all_ind_expressions table in a CURSOR()
    # supquery because of the LONG datatype. We have to query all the column
    # data separately.
    rs = db.query(""" SELECT aic.table_owner
                           , aic.table_name
                           , atc.column_name
                      FROM all_ind_columns aic
                         , all_tab_cols atc
                         , all_ind_expressions aie
                      WHERE aic.index_owner = :o
                        AND aic.index_name = :n
                        AND aic.table_owner = atc.owner
                        AND aic.table_name = atc.table_name
                        AND (aic.column_name = atc.column_name
                          OR aic.column_name = atc.qualified_col_name)
                        AND aic.index_owner = aie.index_owner(+)
                        AND aic.index_name = aie.index_name(+)
                        AND aic.column_position = aie.column_position(+)
                      ORDER BY aic.column_position
                  """, o=name.schema, n=name.obj,
                  oracle_names=['table_owner', 'table_name', 'column_name'])
    columns = [into_database.find(OracleFQN(row['table_owner'],
                                            row['table_name'],
                                            row['column_name']), Column)
               for row in rs]
    return class_(name, database=into_database, table=table, columns=columns,
                  **dict(props))

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

    parts = ["{} SEQUENCE {}".format(operation, name.lower())]
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

    return "CREATE OR REPLACE SYNONYM {} FOR {}".format(name.lower(),
        self.for_object.name.lower())

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
                      FROM all_errors
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
    if hasattr(obj_type, 'namespace'):
      obj_type = obj_type.namespace
    name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)
    if obj.deferred:
      self.log.debug(
          "Adding {}{} as {}".format('deferred ' if obj.deferred else '',
            obj.pretty_name, name))

    if obj_type not in self.objects:
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

    for subobj in obj.subobjects:
      self.add(subobj)

  def find (self, name, obj_type, deferred=True):
    #self.log.debug("Finding {} {}".format(obj_type.__name__, name))
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.name.schema, name)

    if not name.schema:
      name = OracleFQN(self.name.schema, name.obj, name.part)

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

    types = (set(self.objects) | set(other.objects)) - {Column, Constraint}
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

    rs = db.query(""" SELECT object_name
                           , object_type
                           , status
                      FROM all_objects
                      WHERE owner = :o
                        AND subobject_name IS NULL
                        AND generated = 'N'
                        AND object_type IN ( 'FUNCTION'
                                           , 'INDEX'
                                           , 'PACKAGE'
                                           , 'PACKAGE BODY'
                                           , 'PROCEDURE'
                                           , 'SEQUENCE'
                                           , 'SYNONYM'
                                           , 'TABLE'
                                           , 'TYPE'
                                        -- , 'VIEW'
                                           )
                  """, o=owner, oracle_names=['object_name'])

    for obj in rs:
      object_name = OracleFQN(owner, obj['object_name'])
      schema.log.debug(
          "Fetching {} {}".format(obj['object_type'], object_name))

      try:
        class_ = _type_to_class(obj['object_type'])
        db_obj = class_.from_db(object_name, schema.database)
        db_obj.props['status'] = obj['status']
        schema.add(db_obj)
      except _UnexpectedTypeError:
        schema.log.warn("{} [{}]: unexpected type".format(
          obj['object_type'], obj['object_name']))

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
              "    {}".format(schema.objects[obj_type][obj_name].sql(fq=True)))

    return database
