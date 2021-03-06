import logging, os, pickle

from precog import db
from precog.diff import order_diffs
from precog.errors import (AmbiguousNameError, DuplicateIndexConflict,
                           MergeConflict, NonexistentSchemaObjectError,
                           PrecogError, SchemaConflict,
                           UnsatisfiedDependencyError)
from precog.identifier import OracleFQN, OracleIdentifier
from precog.objects import *
from precog.parser import parser
from precog.util import (HasLog, progress_log, pluralize, split_list,
                         _type_to_class_name)


def _plural_type (obj):
  if not isinstance(obj, type):
    obj = type(obj)
  if hasattr(obj, 'namespace'):
    obj = obj.namespace
  return pluralize(2, obj.pretty_type, False)

def _resolve_type (obj):
  if isinstance(obj, type):
    obj_type = obj
  else:
    obj_type = type(obj)
  if hasattr(obj_type, 'namespace'):
    obj_type = obj_type.namespace
  return obj_type

def _freeze_name (name):
  if name.generated:
    # Clear generated flags, etc... so we don't have multiple version of the
    # same name in the schema
    clear_flags = lambda x: x and (OracleIdentifier(x.parts)
                                   if x.parts else str(x))
    name = OracleFQN(name.schema, clear_flags(name.obj), clear_flags(name.part))
  return name

def _to_type (type, name):
  try:
    return globals()[_type_to_class_name(type)]
  except KeyError as e:
    raise PrecogError(
      "{} [{}]: unexpected type".format(type, name)) from e

# When dealing with the cache, we group all PL/SQL objects under the PlsqlCode
# object. However, we need to get the real type back later to look it up in the
# schema, so we hide the type in the name. Perhaps all subclasses of PlsqlCode
# could be stored in one entry in the schema under the PlsqlCode type...
def _mangle_plsql_name (object_type, object_name):
  return object_name.with_(obj=OracleIdentifier(
    "{}.{}".format(object_type.type, object_name.obj), trust_me=True))

def _file_cache_file_name (file_name):
  return "precog_cache_file_{}.pickle".format(
    os.path.splitext(os.path.basename(file_name))[0])

def _db_cache_file_name (schema_name):
  return "precog_cache_db_{}-{}.pickle".format(schema_name, db.dsn)

_cache_version = 'precog cache v4'
def _read_cache (file_name):
  cache_log = logging.getLogger('Cache Loader')
  values = []
  try:
    with open(file_name, 'rb') as cache_file:
      cache_log.info('Found cache file. Reading cache...')
      unpickler = pickle.Unpickler(cache_file)
      version = unpickler.load()
      if version == _cache_version:
        while True:
          values.append(unpickler.load())
      else:
        cache_log.info('Cache file version is obsolete. Ignoring cache.')
  except IOError:
    pass
  except EOFError:
    pass

  return values

def _write_cache (file_name, values):
  with open(file_name, 'wb') as cache_file:
    pickler = pickle.Pickler(cache_file)
    pickler.dump(_cache_version)
    for value in values:
      pickler.dump(value)


class Schema (OracleObject):

  share_namespace = {
        Table,
        #View,
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
    if not isinstance(name, OracleFQN):
      name = OracleFQN(name)

    super().__init__(name, **props)

    # Namespaces
    self.shared_namespace = {}
    self.objects = {}
    self.deferred = {}

  @property
  def name (self):
    return self._name

  @name.setter
  def name (self, value):
    self._name = value
    if hasattr(self, 'objects'):
      def rename (d):
        new_d = {}
        for name, obj in d.items():
          name = name.with_(schema=self.name.schema)
          obj.name = obj.name.with_(schema=self.name.schema)
          new_d[name] = obj
        return new_d

      for obj_type, namespace in self.objects.items():
        self.objects[obj_type] = rename(namespace)
      self.shared_namespace = rename(self.shared_namespace)
      new_deferred = {}
      for key, obj in self.deferred.items():
        if type(key) is tuple:
          key = (key[0].with_(schema=self.name.schema), key[1])
        elif type(key) is frozenset:
          key = frozenset(name.with_(schema=self.name.schema) for name in key)

        obj.name = obj.name.with_(schema=self.name.schema)
        new_deferred[key] = obj
      self.deferred = new_deferred

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
      if hasattr(obj_type, 'namespace'):
        obj_type = obj_type.namespace
      if obj_type not in self.objects:
        self.objects[obj_type] = {}
      self.objects[obj_type][name] = untyped_obj
      if obj_type in self.share_namespace:
        self.shared_namespace[name] = untyped_obj
      self.deferred[(name, obj_type)] = untyped_obj


  def add (self, obj, alternate_name=None):
    if not obj:
      return
    if isinstance(obj, Data):
      # Data objects are attached to a table object, so don't add it here.
      return obj

    obj_type = _resolve_type(obj)

    name = obj.name
    if alternate_name:
      name = alternate_name

    name = _freeze_name(name).with_(schema=self.name.schema)

    self.log.debug(
        "Adding {}{} as {}".format('deferred ' if obj.deferred else '',
          obj.pretty_name, name))

    if obj_type not in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    self._resolve_unknown_type(name, type(obj))

    # Special case for deferred lookups to unique constraints by FK constraints
    if isinstance(obj, UniqueConstraint):
      columns_set = frozenset(col.name.with_(schema=self.name.schema)
                          for col in obj.columns)
      if columns_set in self.deferred:
        self.log.debug(
          "Satisfying deferred Unique Key {} on {} with {}".format(
            self.deferred[columns_set], columns_set, obj))
        self.deferred[columns_set].satisfy(obj)
        obj = self.deferred[columns_set]
        del self.deferred[columns_set]

    if (name, obj_type) in self.deferred:
      # Not a name conflict
      deferred = self.deferred[(name, obj_type)]
      # The object may not actually be deferred, if it's here under an
      # alternate name
      if deferred.deferred:
        self.log.debug("Satisfying deferred {} with {}".format(
          deferred.pretty_name, obj.pretty_name))
        deferred.satisfy(obj)
        # The caller who passed this obj should accept the object returned by
        # this function, so this one should go away, but we don't want any
        # lingering references.
        obj._clear_dependencies()
      del self.deferred[(name, obj_type)]
      obj = deferred
    else:
      if name in namespace:
        if (alternate_name and obj_type is Column and
            abs(namespace[name].internal_column_id -
                obj.internal_column_id) == 1):
          # Two columns right next to each other sharing the same
          # qualified_col_name seem to be related somehow and the lower
          # internal_column_id seems more like the "real" column. Further
          # research here is necessary...
          if namespace[name].internal_column_id < obj.internal_column_id:
            # This one isn't better (i.e. lower) than the one already here, so
            # let's quit now.
            return obj
        else:
          raise SchemaConflict(obj, namespace[name])

      if obj_type in self.share_namespace and name in self.shared_namespace:
        raise SchemaConflict(obj, self.shared_namespace[name])

      # Force this schema name
      obj.name = obj.name.with_(schema=self.name.schema)
      obj.database = self.database
      namespace[name] = obj
      if obj_type in self.share_namespace:
        self.shared_namespace[name] = obj
      if obj.deferred:
        self.deferred[(name, obj_type)] = obj

    if not alternate_name:
      # Special case for object columns. We want to look them up by true name or
      # their qualified name
      if isinstance(obj, Column) and obj.name != obj.qualified_name:
        self.add(obj, obj.qualified_name)

    return obj

  def drop (self, obj):
    obj_type = _resolve_type(obj)
    name = _freeze_name(obj.name)

    if obj_type not in self.objects or name not in self.objects[obj_type]:
      return

    del self.objects[obj_type][name]

    if obj_type in self.share_namespace:
      del self.shared_namespace[name]

    if (isinstance(obj, Column) and obj.name != obj.qualified_name and
        obj.qualified_name in self.objects[obj_type]):
      del self.objects[obj_type][obj.qualified_name]

  def make_deferred (self, obj):
    self.drop(obj)
    obj.become_deferred()
    self.add(obj)

  def drop_invalid_objects (self, invalid_objs):
    self.log.info("Invalidating {}...".format(pluralize(len(invalid_objs),
                                                        'out of date object')))
    for obj in progress_log(invalid_objs, self.log,
                            "Purged {} of invalidated objects."):
      if obj.name.schema == self.name.schema:
        referenced_by = {ref.from_ for ref in obj._referenced_by}
        if referenced_by.difference(invalid_objs):
          if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug("{} will revert to deferred. Referenced by [{}]"
                           .format(obj.pretty_name,
                                   ", ".join(ref_obj.pretty_name
                                             for ref_obj in referenced_by)))
          self.make_deferred(obj)
        else:
          self.log.debug("{} can be discarded.".format(obj.pretty_name))
          # no refences go outside the invalidated set
          obj._clear_dependencies()
          self.drop(obj)

  def __make_fqn (self, name):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.name.schema, name)

    if not name.schema:
      name = name.with_(schema=self.name.schema)

    return name

  def find (self, name, obj_type, deferred=True):
    if isinstance(obj_type, str):
      obj_type = _to_type(obj_type, name)

    if callable(name):
      test = name # For clarity
      if obj_type in self.objects:
        return {obj for obj in self.objects[obj_type].values() if test(obj)}

      return set()

    #self.log.debug("Finding {} {}".format(obj_type.__name__, name))
    name = self.__make_fqn(name)

    if obj_type is Schema and name.schema == self.name.schema:
      return self

    find_type = _resolve_type(obj_type)

    # When you don't know what type you're looking up, it must be in the shared
    # namespace to return a real object. Otherwise it will be deferred.
    if find_type is OracleObject:
      if name in self.shared_namespace:
        return self.shared_namespace[name]

      all_found = [ns[name] for ns in self.objects.values() if name in ns]
      if all_found:
        if len(all_found) == 1:
          return all_found[0]

        raise AmbiguousNameError(name, all_found)

    self._resolve_unknown_type(name, obj_type)

    if find_type in self.objects and name in self.objects[find_type]:
      return self.objects[find_type][name]

    obj = obj_type(name, deferred=True, database=self.database)
    if deferred:
      obj = self.add(obj)
      return obj

    raise NonexistentSchemaObjectError(obj)

  def find_unique_constraint (self, columns, deferred=True):
    column_names = [col.name.with_(schema=self.name.schema) for col in columns]
    columns_set = frozenset(column_names)
    if columns_set in self.deferred:
      return self.deferred[columns_set]

    constraints = None
    if len(columns) == 1:
      constraints = columns[0].unique_constraints
    else:
      table_name = self.__make_fqn(columns[0].name.without_part())
      table = self.find(table_name, Table, deferred)
      if table:
        constraints = table.unique_constraints
        if table.deferred:
          table.columns = columns

    second_best = None
    if constraints:
      for cons in constraints:
        cons_columns = [col.name for col in cons.columns]
        if column_names == cons_columns:
          # Exact match!
          return cons

        if not second_best:
          column_set = set(column_names)
          cons_set = set(cons_columns)
          if column_set == cons_set:
            second_best = cons
            # we won't return here because we may have an exact match with a
            # different constraint. Or maybe not... TODO: test if multiple
            # constraints can have the same column set in different orders.

    if second_best:
      return second_best

    cons = UniqueConstraint(OracleFQN(self.name.schema, GeneratedId()),
                            columns=columns, deferred=True)
    if deferred:
      self.log.debug("Deferring Unique Key on {} as {}".format(columns_set,
                                                               cons))
      self.deferred[columns_set] = cons
      return cons

    raise NonexistentSchemaObjectError(obj)

  def diff (self, other):
    diffs = []
    types = (set(self.objects) | set(other.objects)) - {Column, Constraint}
    for t in progress_log(types, self.log, lambda cur_t:
                          "Compared {{}} of schema {}.{}".format(
                            self.name.schema, " Comparing {}...".format(
                              _plural_type(cur_t))
                            if cur_t else '')):
      rename = t not in {Sequence, Synonym}
      diffs.extend(self.diff_subobjects(other, lambda o: o.objects.get(t, {}),
                                        rename=rename))
    return diffs

  def from_db (self):
    owner = self.name.schema

    self.log.info("Fetching schema {}...".format(owner))

    schema = {
      'objects': db.query_all(
        """ SELECT object_name
                 , object_type
                 , last_ddl_time
            FROM dba_objects
            WHERE owner = :o
              AND subobject_name IS NULL
              AND object_type IN ( 'FUNCTION'
                                 , 'INDEX'
                                 , 'PACKAGE'
                                 , 'PACKAGE BODY'
                                 , 'PROCEDURE'
                                 , 'SEQUENCE'
                                 , 'SYNONYM'
                                 , 'TABLE'
                                 , 'TRIGGER'
                                 , 'TYPE'
                                 , 'TYPE BODY'
                              -- , 'VIEW'
                                 )
            UNION ALL
            SELECT constraint_name
                 , 'CONSTRAINT'
                 , last_change
            FROM dba_constraints
            WHERE owner = :o
              -- Ignore constraints on tables in the recyclebin
              AND NOT (LENGTH(table_name) = 30
                   AND table_name LIKE 'BIN$%')
        """, o=owner, oracle_names=['object_name']),
      'columns': db.query_all(
        """ SELECT table_name
                 , COUNT(*) AS num_columns
            FROM dba_tab_cols
            WHERE owner = :o
              -- Ignore columns on tables in the recyclebin
              AND NOT (LENGTH(table_name) = 30
                   AND table_name LIKE 'BIN$%')
            GROUP BY table_name
        """, o=owner, oracle_names=['table_name']),
      'grants': 0,
      # db.query_one(
      # """ SELECT COUNT(*)
      #     FROM (SELECT DISTINCT owner, table_name
      #           FROM dba_tab_privs
      #           WHERE grantee = :o)
      # """, o=owner),
    }

    self.log.debug("Query complete.")
    total_objects = (len(schema['objects']) + sum(table['num_columns'] for table in schema['columns']) +
                     schema['grants'])

    modified_times = {}
    for object in schema['objects']:
      object_name = OracleFQN(owner, object['object_name'])
      object_type = _to_type(object['object_type'], object_name)
      if issubclass(object_type, PlsqlCode):
        object_name = _mangle_plsql_name(object_type, object_name)
        object_type = PlsqlCode
      if object_type not in modified_times:
        modified_times[object_type] = {}
      modified_times[object_type][object_name] = object['last_ddl_time']

    self.log.info("Schema {} has {}.".format(owner, pluralize(total_objects,
                                                                'object')))
    to_refresh = self.read_cache(modified_times)

    if schema['grants']:
      # Refresh all grants, but only if there are actually any grants out there
      to_refresh[Grant] = None


    change_count = 0
    for obj_type, names in to_refresh.items():
      if obj_type is Column:
        for table in schema['columns']:
          if names is None or table['table_name'] in names:
            change_count += table['num_columns']
      elif names is None:
        if obj_type in modified_times:
          change_count += len(modified_times[obj_type])
        elif obj_type is Grant:
          change_count += schema['grants']
      else:
        change_count += len(names)

    if to_refresh:
      def progress_message (o):
        return "Fetched {{}} of schema {}.{}".format(owner,
          " Currently fetching {}...".format(_plural_type(o))
          if o else '')

      actual = 0
      for obj in progress_log((obj for obj_type, names in to_refresh.items()
                               for obj in obj_type.from_db(
                                 self.name.schema, self.database, names)),
                              self.log, progress_message, count=change_count):
        actual += 1
        self.add(obj)
      self.log.info("Fetching schema {} complete.".format(owner))
      self.cache(modified_times)
    else:
      self.log.info('Using cached schema.')

  def read_cache (self, modified_times):
    to_refresh = dict.fromkeys(modified_times.keys())

    try:
      cached_times, cached_schema = _read_cache(
        _db_cache_file_name(self.name.schema))

      self.props = cached_schema.props
      self.shared_namespace = cached_schema.shared_namespace
      self.objects = cached_schema.objects
      self.deferred = cached_schema.deferred

      refresh_all = set()

      def refresh (obj_names, obj_type):
        if obj_type is not PlsqlCode and issubclass(obj_type, PlsqlCode):
          obj_names = [_mangle_plsql_name(obj_type, obj_name)
                       for obj_name in obj_names]
          obj_type = PlsqlCode
        if hasattr(obj_type, 'namespace'):
          obj_type = obj_type.namespace

        if obj_type not in to_refresh or to_refresh[obj_type] is None:
            to_refresh[obj_type] = set()

        to_refresh[obj_type].update(obj_name.obj for obj_name in obj_names)

      invalid_objs = set()
      for obj_type in modified_times.keys() | cached_times.keys():
        changed = set()
        unchanged = set()

        current_objs = modified_times.get(obj_type, {})
        cached_objs = cached_times.get(obj_type, {})

        changed.update(current_objs.keys() ^ cached_objs.keys())

        for obj_name in current_objs.keys() & cached_objs.keys():
          if current_objs[obj_name] != cached_objs[obj_name]:
            changed.add(obj_name)
          else:
            unchanged.add(obj_name)

        if obj_type is PlsqlCode:
          changed_objs = [
            self.objects[real_obj_type][object_name]
            for real_obj_type, object_name in (
              (_to_type(type_name, object_name), object_name)
              for type_name, object_name in (
                (type_name, OracleFQN(schema, name))
                for schema, (type_name, name) in (
                  (changed_name.schema, changed_name.obj.split('.', 1))
                  for changed_name in changed)))
            if real_obj_type in self.objects and
               object_name in self.objects[real_obj_type]]
        else:
          changed_objs = [self.objects[obj_type][obj_name]
                          for obj_name in changed
                          if obj_type in self.objects and
                          obj_name in self.objects[obj_type]]
        invalid_objs.update(changed_objs)
        for obj in changed_objs:
          refs = {ref.from_ for ref in obj._referenced_by
                  if ref.integrity != Reference.SOFT}
          for ref in refs:
            refresh([ref.name], type(ref))
          invalid_objs.update(refs)

        if unchanged:
          refresh((obj_name
                   for obj_name in (current_objs.keys() - unchanged)),
                  obj_type)
        else:
          to_refresh[obj_type] = refresh_all

      if Grant in self.objects:
        invalid_objs.update(self.objects[Grant].values())

      if invalid_objs:
        self.drop_invalid_objects(invalid_objs)

      # Set to None all types we want to have refreshed in full and delete all
      # types that we won't load at all.
      for obj_type in set(to_refresh):
        if to_refresh[obj_type] is refresh_all:
          to_refresh[obj_type] = None
        elif to_refresh[obj_type] is not None and not to_refresh[obj_type]:
          del to_refresh[obj_type]

    except ValueError:
      pass

    if Table in to_refresh:
      # We don't refresh columns individually, but by the tables they are in
      to_refresh[Column] = to_refresh[Table]
    elif Column in to_refresh:
      # We must have decided we don't need to refresh any tables, so we don't
      # need to refresh any dependent columns either.
      del to_refresh[Column]

    self.log.debug("Refreshing objects: {}".format(to_refresh))
    return to_refresh

  def cache (self, modified_times):
    self.log.info('Caching schema state...')
    _write_cache(_db_cache_file_name(self.name.schema), [modified_times, self])

  def __getstate__ (self):
    state = super().__getstate__()
    state['database'] = None
    return state

class Database (HasLog):

  def __init__ (self, default_schema=None):
    super().__init__()
    self.default_schema = default_schema
    #self.log.debug("Creating with default schema {}".format(default_schema))

    self._ignores = set()
    self._ignore_objs = set()
    self._ignore_schemas = {OracleIdentifier('SYS')}
    self._files = {}
    self._top_file = None

    self.parser = None
    self.schemas = {}
    self.add(Schema(default_schema, database=self))

  @property
  def default_schema (self):
    return self._default_schema

  @default_schema.setter
  def default_schema (self, value):
    if not value:
      value = db.user
    value = OracleIdentifier(value)
    if hasattr(self, '_default_schema'):
      self.rename_schema(self._default_schema, value)
    self._default_schema = value

  def rename_schema (self, from_schema, to_schema):
    from_schema = OracleIdentifier(from_schema)
    to_schema = OracleIdentifier(to_schema)
    if from_schema != to_schema:
      schema = self.schemas[from_schema]
      del self.schemas[from_schema]
      schema.name = OracleFQN(to_schema)
      self.add(schema)

      self._ignores = {(name.with_(schema=to_schema)
                        if name.schema == from_schema else name)
                       for name in self._ignores}
      self._ignore_objs = set()

  def merge_schemas(self, into_schema, source_schema):
    into_schema = self.schemas[into_schema]
    source_schema = self.schemas[source_schema]
    for bucket in source_schema.objects.values():
      for obj in bucket.values():
        try:
          into_schema.add(obj)
        except SchemaConflict:
          raise MergeConflict(into_schema, source_schema)
    del self.schemas[source_schema.name.schema]

  def ignore_schema (self, schema_name):
    schema_name = OracleIdentifier(schema_name)
    self._ignore_schemas.add(schema_name)
    self.came_from_file(schema_name, 'ignore')

  def ignore (self, obj_name):
    if not obj_name.schema:
      obj_name = obj_name.with_(schema=self.default_schema)

    self._ignores.add(obj_name)
    self.came_from_file(obj_name, 'ignore')

  def drop_ignores (self, names):
    split = split_list(names, lambda i: isinstance(i, OracleFQN))
    if True in split:
      self._ignores.difference_update(split[True])
    if False in split:
      self._ignore_schemas.difference_update(split[False])

  def ignores (self):
    if not self._ignore_objs:
      self._ignore_objs = set()
      for obj_name in self._ignores:
        try:
          obj = self.find(obj_name, deferred=False)
          self._ignore_objs.add((type(obj), str(obj.name)))
          self._ignore_objs.update((type(ref), str(ref.name))
                                   for ref in obj._build_dep_set(
                                     lambda self: self._referenced_by,
                                     lambda ref: ref.from_))
        except NonexistentSchemaObjectError:
          pass
    return self._ignore_objs

  def add (self, obj):
    if not obj:
      return obj

    obj.database = self
    schema_name = obj.name.schema
    if isinstance(obj, Schema):
      self.schemas[schema_name] = obj
      obj.database = self
      return

    if not schema_name:
      schema_name = self.default_schema

    if schema_name not in self.schemas:
      self.add(Schema(schema_name))

    obj = self.schemas[schema_name].add(obj)

    self.came_from_file(obj)

    return obj

  def came_from_file (self, obj, kind=None):
    if self.parser:
      if kind:
        obj = (kind, obj)
      objs = self._files.get(self.parser.source_file)
      if not objs:
        objs = []
        self._files[self.parser.source_file] = objs
      objs.append(obj)

  def add_file (self, filename):
    if not self.parser:
      self.parser = parser.SqlPlusFileParser(self._files.keys())

    included = self.parser.parse(filename, self)

    for file in self.parser.parsed_files:
      if file not in self._files:
        # Maybe there were no objects parsed from this file, but we still need
        # to know about it because it's probably part of the include tree
        self._files[file] = []

    return included

  def __make_fqn (self, name):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.default_schema, name)

    if not name.schema:
      name = OracleFQN(self.default_schema, name.obj, name.part)

    if name.schema not in self.schemas:
      self.add(Schema(name.schema, database=self))

    return name

  def find (self, name, obj_type=OracleObject, deferred=True):
    if isinstance(obj_type, str):
      obj_type = _to_type(obj_type, name)

    if obj_type is OracleObject and isinstance(name, list):
      # Try and resolve a very ambiguous name
      schema = None
      obj = None
      part = None

      if len(name) > 1 and name[0] in self.schemas:
        schema = name.pop(0)
      else:
        schema = self.default_schema

      obj = name.pop(0)
      found = self.schemas[schema].find(OracleFQN(schema, obj), OracleObject,
                                        False)
      part = name
      name = OracleFQN(schema, obj, part)
      if found:
        if part and isinstance(found, Table):
            column = self.schemas[schema].find(name, Column, deferred)
            if column:
              return column

        return found


    if callable(name):
      test = name # For clarity
      return {obj for schema in self.schemas.values()
              for obj in schema.find(test, obj_type)}

    if obj_type is Schema and not isinstance(name, OracleFQN):
      name = OracleFQN(name)

    name = self.__make_fqn(name)
    return self.schemas[name.schema].find(name, obj_type, deferred)

  def find_unique_constraint (self, columns, deferred=True):
    return (self.schemas[self.__make_fqn(columns[0].name).schema]
            .find_unique_constraint(columns, deferred))

  def validate (self):
    self.log.info('Validating referential integrity...')
    ignores = self.ignores()
    unsatisfied = [obj for name, schema in self.schemas.items()
                   if name not in self._ignore_schemas
                   for obj in schema.deferred.values()
                   if (type(obj), str(obj.name)) not in ignores and
                     # Deferred object referred to only by soft references
                     # aren't a big deal
                     any(ref for ref in obj._referenced_by
                         if ref.integrity != Reference.SOFT)]

    if unsatisfied:
      raise UnsatisfiedDependencyError(unsatisfied)

    for schema in self.schemas.values():
      if Index in schema.objects:
        indexes = {}
        for idx in schema.objects[Index].values():
          if idx.table not in indexes:
            indexes[idx.table] = {}
          cols = tuple(idx.columns)
          if cols in indexes[idx.table]:
            raise DuplicateIndexConflict(idx, indexes[idx.table][cols])
          indexes[idx.table][cols] = idx

  def from_db (self):
    try:
      to_load = set(self.schemas.keys())
      loaded = set()
      while to_load:
        for schema_name in to_load:
          if schema_name not in self._ignore_schemas:
            self.schemas[schema_name].from_db()

        loaded.update(to_load)
        to_load = self.schemas.keys() - loaded

      self.validate()
    except PrecogError:
      self.log.error(
        'The Oracle database has errors. This is probably the fault of Precog.')
      raise

  def diff_to_db (self, connection_string):
    self.log.info('Loading current database state...')

    # Perform all schema aliasing on self, before passing any attributes on to
    # the oracle_database. The oracle_database will therefore be fully aliased.
    self.default_schema = schema_alias(self.default_schema)
    for schema_name in set(self.schemas):
      aliased_schema_name = schema_alias(schema_name)
      if schema_name != aliased_schema_name:
        if aliased_schema_name in self.schemas:
          self.merge_schemas(aliased_schema_name, schema_name)
        else:
          self.rename_schema(schema_name, aliased_schema_name)

    db.connect(connection_string)

    oracle_database = Database(self.default_schema)
    oracle_database._ignores = self._ignores
    oracle_database._ignore_schemas = self._ignore_schemas

    for schema_name in self.schemas:
      if (schema_name not in self._ignore_schemas and
          schema_name not in oracle_database.schemas):
        oracle_database.add(Schema(schema_name))
    oracle_database.from_db()

    self.log.info('Comparing database definition to current database state...')

    diffs = []
    for schema_name in self.schemas:
      if schema_name not in self._ignore_schemas:
        diffs.extend(self.schemas[schema_name].diff(
          oracle_database.schemas[schema_name]))

    if diffs:
      diffs = order_diffs(diffs)

    return diffs

  @classmethod
  def dump_schema (class_, connection_string, schema_name, tables=None):
    db.connect(connection_string)

    oracle_database = Database()

    diffs = []
    db_schema = Schema(schema_name, database=oracle_database)
    oracle_database.add(db_schema)

    if tables:
      tables = {OracleIdentifier(table_name): ([c.strip()
                                                for c in columns[0].split(',')]
                                               if len(columns) else None)
                for table_name, *columns in (table.split(':', 1)
                                             for table in tables)}
      for table in Table.from_db(db_schema.name.schema, oracle_database,
                                 tables):
        db_schema.add(table)

      for table_name, columns in tables.items():
        table = db_schema.find(table_name, Table, False)
        if columns:
          for column_name in columns:
            db_schema.find(table.name.with_(part=column_name), Column, False)
        Data.from_db(table, columns)
        diffs.append(Diff(["-- Data for {}".format(table_name)] +
                          [datum.sql(fq=False, columns=columns)
                           for datum in table.data], produces=set(table.data)))
    else:
      db_schema.from_db()

      # Set index ownership for all unique constraints
      if Constraint in db_schema.objects:
        for cons in db_schema.objects[Constraint].values():
          if isinstance(cons, UniqueConstraint):
            cons.index_ownership = UniqueConstraint.FULL_INDEX_CREATE

      diffs = db_schema.diff(Schema(schema_name, database=Database()))

    if diffs:
      diffs = order_diffs(diffs)

    return diffs

  @classmethod
  def from_file (class_, filename, default_schema=None):
    database = class_.read_cache(filename.name, default_schema)

    if not database:
      database = class_(default_schema)
      database.add_file(filename)
      database._top_file = filename.name
      database.cache()

    database.validate()

    #if database.log.isEnabledFor(logging.DEBUG):
      #for schema in database.schemas.values():
        #database.log.debug("Schema {}".format(schema.name))
        #for obj_type in schema.objects:
          #database.log.debug("  {}s:".format(obj_type.__name__))
          #for obj_name in sorted([obj_name for obj_name in
              #schema.objects[obj_type]], key=lambda n: str(n)):
            #database.log.debug(
              #"    {}".format(schema.objects[obj_type][obj_name].sql(fq=True)))

    return database

  @classmethod
  def read_cache (class_, file_name, default_schema=None):
    cache_log = logging.getLogger('Cache Loader')
    try:
      cache_file_name = _file_cache_file_name(file_name)
      cached_files, database = _read_cache(cache_file_name)

      out_of_date_files = []
      saw_top_file = False
      for file, cached_mtime in cached_files:
        if file == file_name:
          saw_top_file = True
        current_mtime = None
        try:
          current_mtime = os.stat(file).st_mtime
        except OSError:
          pass
        if current_mtime != cached_mtime:
          out_of_date_files.append(file)
      if not saw_top_file:
        cache_log.info('Cache in file "{}" does not correspond with {}. '
                       'Ignoring cache.'
                       .format(cache_file_name, file_name))
        return

      if not database._files.keys() - out_of_date_files:
        # Everything is out of date, so there's no reason to use the cache
        cache_log.info('Entire cache is out of date.')
        return

      database._top_file = file_name
      # reestablish Schema links back to Database
      for schema in database.schemas.values():
        schema.database = database

      database.default_schema = default_schema

      if out_of_date_files:
        database.log.info("Refreshing cache with {}..."
                          .format(pluralize(len(out_of_date_files),
                                                'out of date file')))
        database.refresh_files(out_of_date_files)
      else:
        database.log.info('Using cached definition.')

      return database
    except ValueError:
      pass

  def cache (self):
    self.log.info('Caching parsed definition...')
    _write_cache(_file_cache_file_name(self._top_file),
                 [[(file, os.stat(file).st_mtime) for file in self._files],
                  self])

  def drop_files (self, files):
    invalid_objs = set()
    outdated_includes = set()
    for file in files:
      if file in self._files:
        split = split_list(self._files[file],
                           lambda i: i[0] if isinstance(i, tuple) else None)
        if 'ignore' in split:
          self.drop_ignores(i[1] for i in split['ignore'])
        if 'include' in split:
          outdated_includes.update(i[1] for i in split['include'])
        if None in split:
          invalid_objs.update(split[None])
        del self._files[file]

    schema_names = {obj.name.schema for obj in invalid_objs}

    for schema_name in schema_names:
      self.schemas[schema_name].drop_invalid_objects(invalid_objs)

    return outdated_includes

  def refresh_files (self, files):
    outdated_includes = self.drop_files(files)

    files = [file for file in files if file not in outdated_includes]

    included = []
    for file in files:
      included.extend(self.add_file(file))

    while True:
      outdated_includes = self.drop_files(
        outdated_includes.difference(included))
      if not outdated_includes:
        break

    self.cache()

  def __getstate__ (self):
    state = super().__getstate__()
    state['parser'] = None
    state['_ignore_objs'] = None
    return state
