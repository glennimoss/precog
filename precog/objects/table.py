import itertools

from precog import db
from precog.diff import Commit, Diff
from precog.identifier import OracleFQN
from precog.objects.base import OracleObject
from precog.objects.column import Column
from precog.objects.constraint import Constraint
from precog.objects.data import Data
from precog.objects.index import Index
from precog.objects.has.columns import OwnsColumns
from precog.objects.has.constraints import HasConstraints
from precog.objects.has.prop import HasProp
from precog.objects.has.user_type import HasUserType
from precog.objects.plsql import Type

_HasData_ = HasProp('data', assert_collection=list, assert_type=Data)
class _HasData (_HasData_):

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)

    if self.data:
      Data.from_db(other)

      inserts = self.diff_subobjects(other, lambda o: o.data,
                                     lambda o: o._comp(True), rename=False)
      if inserts:
        diffs.extend(inserts)
        diffs.append(Commit(inserts))

    return diffs

  def _collect_dups (self, objs):
    dups = {}
    for dup in objs:
      dups.setdefault(dup._comp(), [dup, 0])[1] += 1

    return dups

  def add_dup_subobjects (self, subobjects):
    if not isinstance(subobjects[0], Data):
      return super().add_dup_subobjects(subobjects)

    dups = self._collect_dups(subobjects)

    diffs = []
    for dup, count in dups.values():
      create = dup.create()
      create.sql *= count
      diffs.append(create)

    return diffs

  def drop_subobjects (self, subobjects):
    if self.props['partial_data']:
      subobjects = [o for o in subobjects if not isinstance(o, Data)]
    return super().drop_subobjects(subobjects)

  def drop_dup_subobjects (self, subobjects):
    diffs = []

    not_data = []
    data = []
    for obj in subobjects:
      if isinstance(subobjects[0], Data) and not self.props['partial_data']:
        data.append(obj)
      else:
        not_data.append(obj)
    if not_data:
      diffs.extend(super().drop_dup_subobjects(subobjects))

    dups = self._collect_dups(data)

    for dup, count in dups.values():
      drop = dup._drop()
      drop.sql[0] += " AND ROWNUM < {}".format(count + 1)
      diffs.append(drop)

    return diffs

class Table (HasConstraints, _HasData, OwnsColumns, OracleObject):

  def __new__ (class_, *args, **props):
    if 'table_type' in props and props['table_type']:
      class_ = ObjectTable
    return super().__new__(class_)

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
          # We don't just do a .add() because we need to trigger the setter
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
    for datum in self.data:
      datum.name = self.name.with_(part=datum.name.part)

  def __repr__ (self):
    return super().__repr__(data=self.data)

  def add_data (self, columns, values):
    data = Data(self, columns, values)
    self.data.append(data)
    return data

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
    # TODO: should not include unique constraints who don't own their indexes.
    # They would need to be added after the creation of the index.
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
  def from_db (class_, schema, into_database, table_names=None):
    table_filter = db.filter_clause('table_name', table_names)
    into_database.log.debug("Querying for tables {} from DB...".format(
      "(all)" if table_names is None else ", ".join(table_names)))
    rs = db.query(""" SELECT table_name
                           , table_type
                           , CASE WHEN table_type_owner = 'PUBLIC'
                                    OR table_type_owner LIKE '%SYS' THEN NULL
                                  ELSE table_type_owner
                             END AS table_type_owner
                           , tablespace_name
                           , iot_type
                           , nested
                           , ( SELECT CAST(COLLECT(column_name ORDER BY dtc.internal_column_id) AS gt_string_table)
                               FROM dba_tab_cols dtc
                               WHERE dtc.owner = dat.owner
                                 AND dtc.table_name = dat.table_name
                             ) AS columns
                           , ( SELECT CAST(COLLECT(constraint_name) AS gt_string_table)
                               FROM ( SELECT constraint_name
                                      FROM dba_cons_columns dcc
                                      WHERE dcc.owner = dat.owner
                                        AND dcc.table_name = dat.table_name
                                      GROUP BY constraint_name
                                      HAVING COUNT(*) > 1)
                             ) AS constraints
                      FROM dba_all_tables dat
                      WHERE owner = :o
                         {}
                  """.format(table_filter), o=schema,
                  oracle_names=['table_name', 'columns', 'constraints', 'tablespace_name'])

    into_database.log.debug("Cursor obtained")
    for row in rs:
      props = {'tablespace_name': row['tablespace_name'],
               'table_type': row['table_type']}
      table_name = OracleFQN(schema, row['table_name'])
      into_database.log.debug("Processing table {}".format(table_name))
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
                                                       column_name),
                                             Column)
                          for column_name in row['columns']]

      props['constraints'] = {
        into_database.find(OracleFQN(table_name.schema, constraint_name), Constraint)
        for constraint_name in row['constraints']}

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
