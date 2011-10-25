from precog.objects.base import OracleObject
from precog.objects.has.columns import HasColumns

class Index (HasColumns, OracleObject):

  def __init__ (self, name, unique=None, **props):
    super().__init__(name, **props)
    if unique is not None:
      self.unique = unique

  @property
  def unique (self):
    return self.props['uniqueness'] == 'UNIQUE'

  @unique.setter
  def unique (self, value):
    self.props['uniqueness'] = 'UNIQUE' if value else 'NONUNIQUE'

  @property
  def table (self):
    if self.columns:
      return self.columns[0].table
    return None

  def _sql (self, fq=True):
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
    if 'index_type' in self.props and self.props['index_type'].endswith('/REV'):
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
                        -- , table_owner
                        -- , table_name
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
    if rs['index_type'].find('NORMAL') == -1:
      into_database.log.warn(
        "Index {} is of unsupported type {}".format(name, rs['index_type']))
      rs['index_type'] = 'NORMAL'
      #raise UnimplementedFeatureError(
      #  "Index {} is of unsupported type {}".format(name, rs['index_type']))
    #*props, (_, table_owner), (_, table_name), (_, columns) = rs.items()
    *props, (_, columns) = rs.items()

    columns = [into_database.find(OracleFQN(col['table_owner'],
                                            col['table_name'],
                                            col['column_name']), Column)
               for col in columns]
    return class_(name, database=into_database, columns=columns, **dict(props))
