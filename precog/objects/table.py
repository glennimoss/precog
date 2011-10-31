from precog import db
from precog.diff import Commit, Diff
from precog.identifier import *
from precog.objects.base import OracleObject, SkippedObject
from precog.objects.column import Column
from precog.objects.constraint import Constraint
from precog.objects.index import Index
from precog.objects.has.columns import HasColumns, OwnsColumns
from precog.objects.has.constraints import HasConstraints
from precog.objects.has.prop import HasProp
from precog.objects.has.user_type import HasUserType
from precog.objects.plsql import Type
from precog.util import InsensitiveDict

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
    return InsensitiveDict(zip((col.name.part.lower()
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

_HasData = HasProp('data', assert_collection=list, assert_type=Data)
class Table (HasConstraints, _HasData, OwnsColumns, OracleObject):

  def __new__ (class_, *args, **props):
    if 'table_type' in props and props['table_type']:
      class_ = ObjectTable
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, **props):
    self._data = []
    super().__init__(name, column_reference=None, **props)

  @OwnsColumns.columns.setter
  def columns (self, value):
    OwnsColumns.columns.__set__(self, value)
    if value:
      for column in value:
        column.table = self

  @HasConstraints.constraints.setter
  def constraints (self, value):
    if value:
      cols = {col.name: col for col in self.columns}
      column_constraints = set()
      for cons in value:
        if len(cons.columns) == 1:
          # add this constraint to the appropriate column
          col = cols[cons.columns[0].name]
          # We don'tjust do a .add() because we need to trigger the setter
          col.constraints = col.constraints | {cons}

          column_constraints.add(cons)
      value.difference_update(column_constraints)

    HasConstraints.constraints.__set__(self, value)

  @property
  def name (self):
    return self._name

  @name.setter
  def name (self, value):
    self._name = value
    # Reset the names of all the columns
    self.columns = self._columns

  def __repr__ (self):
    return super().__repr__(data=self.data)

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
             if col.props['hidden_column'] != 'YES']
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

      diffs.extend(diff for idx in other.database.find(lambda obj:
                                                         obj.table == other,
                                                       Index)
                   for diff in idx.rebuild())

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
                           , iot_type
                           , nested
                      FROM dba_all_tables
                      WHERE owner = :o
                        AND table_name = :t
                  """, o=name.schema, t=name.obj,
                  oracle_names=['tablespace_name'])
    if not rs:
      into_database.log.warn("Table not found for {}".format(name))
      return None
    props = rs[0]
    if props['iot_type'] is not None:
      # TODO: currently ignoring index-organized tables
      into_database.log.info(
        "Table {} is an index-organized table. Skipping...".format(name))
      return SkippedObject
    if props['nested'] == 'YES':
      # TODO: assuming that nested tables are managed by their parent tables
      into_database.log.info(
        "Table {} is a nested table. Skipping...".format(name))
      return SkippedObject
    del props['iot_type']
    del props['nested']
    if props['table_type_owner']:
      props['user_type'] = into_database.find(
        OracleFQN(props['table_type_owner'], props['table_type']), Type)
      del props['table_type_owner']
    elif not props['table_type']:
      props['columns'] = Column.from_db(name, into_database)

    props['constraints'] = Constraint.from_db(name, into_database)

    return class_(name, database=into_database, **props)

class ObjectTable (HasUserType, HasProp('table_type', assert_type=str), Table):
  namespace = Table

  @HasUserType.user_type.setter
  def user_type (self, value):
    HasUserType.user_type.__set__(self, value)
    if value:
      self.table_type = self.user_type.name.lower()

  def _sub_sql (self):
    return " OF {}".format(self.table_type)
