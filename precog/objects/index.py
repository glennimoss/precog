from precog import db
from precog.diff import Diff
from precog.identifier import *
from precog.objects.base import OracleObject, SkippedObject
from precog.objects.has.columns import HasColumns, HasTableFromColumns

class Index (HasTableFromColumns, HasColumns, OracleObject):

  def __init__ (self, name, unique=None, reverse=None, **props):
    super().__init__(name, **props)
    if unique is not None:
      self.unique = unique

  @HasColumns.columns.setter
  def colunms (self, value):
    HasColumns.columns.__set__(self, value)
    if (self.props['index_type'] and
        [col for col in self.columns if isinstance(col, VirtualColumn)]):
      self.props['index_type'] = "FUNCTION-BASED {}".format(
        self.props['index_type'])

  @property
  def unique (self):
    return self.props['uniqueness'] == 'UNIQUE'

  @unique.setter
  def unique (self, value):
    self.props['uniqueness'] = 'UNIQUE' if value else 'NONUNIQUE'

  def _sql (self, fq=True):
    try:
      name = self.name.obj
      if fq:
        name = self.name
      parts = ['CREATE']
      if self.unique:
        parts.append('UNIQUE')
      parts.append('INDEX')
      parts.append(name.lower())
      parts.append('ON')
      parts.append(self.table.name.lower())
      parts.append('(')
      parts.append(', '.join(c.sql(full_def=False) for c in self.columns))
      parts.append(')')
      if ('index_type' in self.props and
          self.props['index_type'].endswith('/REV')):
        parts.append('REVERSE')
      if self.props['tablespace_name']:
        parts.append('TABLESPACE')
        parts.append(self.props['tablespace_name'].lower())
    except Exception as e:
      self.log.error(
        "Index {} has colums {} had the problem {}".format(self.pretty_name,
                                                           self.columns, e))

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
                           , CURSOR(
                               SELECT table_owner
                                    , table_name
                                    , column_name
                               FROM dba_ind_columns aic
                               WHERE aic.index_owner = ai.owner
                                 AND aic.index_name = ai.index_name
                               ORDER BY aic.column_position
                             ) AS columns
                      FROM dba_indexes ai
                      WHERE owner = :o
                        AND index_name = :n
                  """, o=name.schema, n=name.obj,
                  oracle_names=['tablespace_name', 'table_owner', 'table_name',
                    'column_name'])
    if not rs:
      return None
    rs = rs[0]
    if rs['index_type'] == 'IOT - TOP':
      into_database.log.info(
        "Index {} is for an index-organized table. Skipping...".format(name))
      return SkippedObject

    if rs['index_type'].find('NORMAL') == -1:
      into_database.log.warn(
        "Index {} is of unsupported type {}".format(name, rs['index_type']))
      return None
    *props, (_, columns) = rs.items()

    from precog.objects.column import Column
    columns = [into_database.find(OracleFQN(col['table_owner'],
                                            col['table_name'],
                                            col['column_name']), Column)
               for col in columns]
    # An index without columns is hardly an index at all!
    if not columns:
      into_database.log.warn(
        "Index {} has no columns. Index skipped.".format(name))
      return None
    return class_(name, database=into_database, columns=columns, **dict(props))
