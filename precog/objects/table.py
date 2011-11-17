import itertools

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
    self.expressions = []
    for i, exp in enumerate(expressions):
      exp = Data.numerify(exp, self.columns[i].is_number)
      self.expressions.append(exp)

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    return self.table.name == other.table.name and self._comp() == other._comp()

  def __ne__ (self, other):
    return not self == other

  def __hash__ (self):
    return hash((self.table.name, self._comp()))

  def _comp (self):
    """ A tuple view for hashing, comparing, etc. """
    return tuple(sorted(tup for tup in self.values().items()
                        if tup[1] is not None))

  def values (self, normalize=False):
    return InsensitiveDict(zip((col.name.part.lower() for col in self.columns),
                               self.expressions))

  def _sql (self, fq=True):
    table_name = self.table.name
    if not fq:
      table_name = table_name.obj
    values = self.values(True)
    return "INSERT INTO {} ({}) VALUES ({})".format(table_name.lower(),
      ", ".join(values.keys()), ", ".join(str(val) for val in values.values()))

  def _drop (self):
    return Diff("DELETE FROM {} WHERE {}".format(
      self.table.name.lower(), " AND ".join(
        " = ".join((col, str(val)))
        if val is not None else "{} IS NULL".format(col)
        for col, val in self.values(True).items())))

  def diff (self, other, **kwargs):
    return []

  @staticmethod
  def numerify (value, col_is_number):
    if isinstance(value, str):
      if col_is_number or not (value.startswith("'") and value.endswith("'")):
        val = value.strip("'")
        try:
          num = float(val)
          if num.is_integer():
            num = int(num)
          if not col_is_number:
            num = "'{}'".format(num)
          return num
        except ValueError:
          pass
    return value

  @staticmethod
  def escape (value, col_is_number):
    if isinstance(value, str):
      return "'{}'".format(value.replace("'", "''"))
    return Data.numerify(value, col_is_number)

  @classmethod
  def from_db (class_, table):
    if not table.data:
      rs = db.query_all(""" SELECT *
                            FROM {}
                        """.format(table.name))

      if rs:
        columns = [table.database.find(
          OracleFQN(table.name.schema, table.name.obj, column_name), Column)
          for column_name in rs[0]]

        for row in rs:
          table.add_data(columns, [Data.escape(col, columns[i].is_number)
                                   for i, col in enumerate(row.values())])

_HasData_ = HasProp('data', assert_collection=list, assert_type=Data)
class _HasData (_HasData_):

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)

    if self.data:
      Data.from_db(other)

    inserts = self.diff_subobjects(other, lambda o: o.data, lambda o: o._comp())
    if inserts:
      diffs.extend(inserts)
      diffs.append(Commit(inserts))

    return diffs

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
    parts.extend(cons.sql() for cons in self.constraints)
    return "\n  ( {}\n  )".format("\n  , ".join(parts))

  @property
  def sql_produces (self):
    return {self}.union(product for obj in itertools.chain(self.columns,
                                                           self.constraints,
                                                           self.data)
                        for product in obj.sql_produces)

  def create (self):
    diff = super().create()

    if self.data:
      diff.sql.extend(datum.sql() for datum in self.data)
      diff.sql.append('COMMIT')

    return diff

  def diff (self, other, **kwargs):
    diffs = super().diff(other, recreate=False, **kwargs)

    prop_diffs = self._diff_props(other)
    # Remove subobject entries
    for prop in ('columns', 'constraints', 'data'):
      if prop in prop_diffs:
        del prop_diffs[prop]

    if len(prop_diffs) == 1 and 'tablespace_name' in prop_diffs:
      move_diff = Diff("ALTER TABLE {} MOVE TABLESPACE {}"
                       .format(other.name.lower(),
                               self.props['tablespace_name'].lower()),
                       produces=self)
      diffs.append(move_diff)

      for idx in other.database.find(lambda obj: obj.table == other, Index):
        for diff in idx.rebuild():
          diff.add_dependencies(move_diff)
          diffs.append(diff)

    return diffs

  @classmethod
  def from_db (class_, schema, into_database):
    rs = db.query(""" SELECT table_name
                           , table_type
                           , CASE WHEN table_type_owner = 'PUBLIC'
                                    OR table_type_owner LIKE '%SYS' THEN NULL
                                  ELSE table_type_owner
                             END AS table_type_owner
                           , tablespace_name
                           , iot_type
                           , nested
                           , CURSOR(
                               SELECT column_name
                               FROM dba_tab_cols dtc
                               WHERE dtc.owner = dat.owner
                                 AND dtc.table_name = dat.table_name
                               ORDER BY dtc.internal_column_id
                             ) AS columns
                           , CURSOR(
                               SELECT constraint_name
                               FROM dba_cons_columns dcc
                               WHERE dcc.owner = dat.owner
                                 AND dcc.table_name = dat.table_name
                               GROUP BY constraint_name
                               HAVING COUNT(*) > 1
                             ) AS constraints
                      FROM dba_all_tables dat
                      WHERE owner = :o
                  """, o=schema, oracle_names=['table_name', 'column_name',
                                               'tablespace_name'])

    for row in rs:
      props = {'tablespace_name': row['tablespace_name'],
               'table_type': row['table_type']}
      table_name = OracleFQN(schema, row['table_name'])
      if row['iot_type'] is not None:
        # TODO: currently ignoring index-organized tables
        into_database.log.debug(
          "Table {} is an index-organized table. Skipping...".format(
            table_name))
        continue
      if row['nested'] == 'YES':
        # TODO: assuming that nested tables are managed by their parent tables
        into_database.log.debug(
          "Table {} is a nested table. Skipping...".format(table_name))
        continue
      if row['table_type_owner']:
        props['user_type'] = into_database.find(
          OracleFQN(row['table_type_owner'], row['table_type']), Type)

      props['columns'] = [into_database.find(OracleFQN(table_name.schema,
                                                       table_name.obj,
                                                       col['column_name']),
                                             Column)
                          for col in row['columns']]

      props['constraints'] = {
        into_database.find(OracleFQN(table_name.schema,
                                     cons['constraint_name']),
                           Constraint)
        for cons in row['constraints']}

      yield class_(table_name, database=into_database,
                        create_location=(db.location,), **props)
    rs.close()

class ObjectTable (HasUserType, HasProp('table_type', assert_type=str), Table):
  namespace = Table

  @HasUserType.user_type.setter
  def user_type (self, value):
    HasUserType.user_type.__set__(self, value)
    if value:
      self.table_type = self.user_type.name.lower()

  def _sub_sql (self):
    return " OF {}".format(self.table_type)
