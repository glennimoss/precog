from precog.objects._misc import *
from precog.objects.base import OracleObject
from precog.objects.plsql import *
from precog.objects.sequence import Sequence
from precog.objects.synonym import Synonym
from precog.objects.table import Table
from precog.util import HasLog

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
      if hasattr(obj_type, 'namespace'):
        obj_type = obj_type.namespace
      if obj_type not in self.objects:
        self.objects[obj_type] = {}
      self.objects[obj_type][name] = untyped_obj
      self.deferred[(name, obj_type)] = untyped_obj

  def add (self, obj, alternate_name=None):
    if not obj:
      return

    obj_type = type(obj)
    if hasattr(obj_type, 'namespace'):
      obj_type = obj_type.namespace
    name = obj.name
    if alternate_name:
      name = alternate_name
    name = OracleFQN(self.name.schema, name.obj, name.part)

    print(name.obj)
    if name.obj is None:
      import pdb
      pdb.set_trace()
    self.log.debug(
        "Adding {}{} as {}".format('deferred ' if obj.deferred else '',
          obj.pretty_name, name))

    if obj_type not in self.objects:
      self.objects[obj_type] = {}
    namespace = self.objects[obj_type]

    self._resolve_unknown_type(name, type(obj))

    if (name, obj_type) in self.deferred:
      # Not a name conflict
      deferred = self.deferred[(name, obj_type)]
      # The object may not actually be deferred, if it's here under an
      # alternate name
      if deferred.deferred:
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
        # Force this schema name
        obj.name = OracleFQN(self.name.schema, obj.name.obj, obj.name.part)
        obj.database = self.database
        namespace[name] = obj
        if obj_type in self.share_namespace:
          self.shared_namespace[name] = obj

    if not alternate_name:
      for subobj in obj.subobjects:
        self.add(subobj)

      # Special case for object columns. We want to look them up by true name or
      # their qualified name
      if isinstance(obj, Column) and obj.name != obj.qualified_name:
        self.add(obj, obj.qualified_name)

    # Special case for deferred lookups to unique constraints by FK constraints
    if isinstance(obj, UniqueConstraint):
      columns_tup = tuple(col.name for col in obj.columns)
      if columns_tup in self.deferred:
        self.log.debug(
          "Satisfying deferred Unique Key {} on {} with {}".format(
            self.deferred[columns_tup], columns_tup, obj))
        self.deferred[columns_tup].satisfy(obj)
        del self.deferred[columns_tup]

  def __make_fqn (self, name) :
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.name.schema, name)

    if not name.schema:
      name = OracleFQN(self.name.schema, name.obj, name.part)

    return name

  def find (self, name, obj_type, deferred=True):
    if callable(name):
      test = name # For clarity
      if obj_type in self.objects:
        return {obj for obj in self.objects[obj_type].values() if test(obj)}

      return set()

    #self.log.debug("Finding {} {}".format(obj_type.__name__, name))
    name = self.__make_fqn(name)

    find_type = (obj_type.namespace if hasattr(obj_type, 'namespace')
                 else obj_type)
    # When you don't know what type you're looking up, it must be in the shared
    # namespace to return a real object. Otherwise it wil be deferred.
    if find_type is OracleObject and name in self.shared_namespace:
      return self.shared_namespace[name]

    self._resolve_unknown_type(name, obj_type)

    if find_type in self.objects and name in self.objects[find_type]:
      return self.objects[find_type][name]

    if deferred:
      obj = obj_type(name, deferred=True)
      self.add(obj)
      self.deferred[(name, find_type)] = obj
      return obj

    return None

  def find_unique_constraint (self, columns, deferred=True):
    column_names = [col.name for col in columns]
    columns_tup = tuple(column_names)
    if columns_tup in self.deferred:
      return self.deferred[columns_tup]

    if len(columns) == 1:
      constraints = columns[0].unique_constraints
    else:
      table_name = self.__make_fqn(OracleFQN(columns[0].name.schema,
                                             columns[0].name.obj))
      table = self.find(table_name, Table)
      constraints = table.unique_constraints

    second_best = None
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

    if deferred:
      cons = UniqueConstraint(OracleFQN(self.name.schema, GeneratedId()),
                              columns=columns, deferred=True)
      self.log.debug("Deferring Unique Key on {} as {}".format(columns_tup,
                                                               cons))
      self.deferred[columns_tup] = cons
      return cons

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
                           , generated
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
                                           , 'TYPE'
                                        -- , 'VIEW'
                                           )
                  """, o=owner, oracle_names=['object_name'])

    for obj in rs:
      object_name = OracleFQN(owner,
              OracleIdentifier(obj['object_name'],
                               generated=(obj['generated'] == 'Y')))
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
    sql_parser = parser.file_parser(filename)
    sql_parser.sqlplus_file(self)
    num_errors = sql_parser.getNumberOfSyntaxErrors()
    if num_errors:
      # we don't want to compare to the database when our spec is incomplete
      raise ParseError(num_errors)

  def __make_fqn (self, name):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(self.default_schema, name)

    if not name.schema:
      name = OracleFQN(self.default_schema, name.obj, name.part)

    if name.schema not in self.schemas:
      self.schemas[name.schema] = Schema(name.schema, database=self)

    return name

  def find (self, name, obj_type=OracleObject, deferred=True):
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


    name = self.__make_fqn(name)
    return self.schemas[name.schema].find(name, obj_type, deferred)

  def find_unique_constraint (self, columns, deferred=True):
    return (self.schemas[self.__make_fqn(columns[0].name).schema]
            .find_unique_constraint(columns, deferred))

  def validate (self):
    self.log.info('Validating referential integrity')
    unsatisfied = [obj for schema in self.schemas.values()
        for obj in schema.deferred.values()]

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

  def diff_to_db (self, connection_string):
    self.validate()

    self.log.info('Comparing database definition to current database state')

    db.connect(connection_string)

    oracle_database = Database()

    diffs = []
    for schema_name in self.schemas:
      db_schema = Schema(schema_name, database=oracle_database)
      oracle_database.add(db_schema)
      Schema.from_db(db_schema)

    #for schema in oracle_database.schemas.values():
      #Schema.from_db(schema)

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
