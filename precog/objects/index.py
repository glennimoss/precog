from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects.base import OracleObject, SkippedObject
from precog.objects.has.columns import HasColumns, HasTableFromColumns
from precog.objects.has.extradeps import HasExtraDeps

class Index (HasExtraDeps, HasTableFromColumns, HasColumns, OracleObject):

  def __init__ (self, name, unique=None, reverse=None, **props):
    super().__init__(name, **props)
    if unique is not None:
      self.unique = unique

  @HasColumns.columns.setter
  def columns (self, value):
    from precog.objects.column import VirtualColumn
    HasColumns.columns.__set__(self, value)
    if (self.props['index_type'] and
        [col for col in self.columns if isinstance(col, VirtualColumn)]):
      self.props['index_type'] = "FUNCTION-BASED {}".format(
        self.props['index_type'].split()[-1])

  def _eq_columns (self, other):
    for col in self.columns:
      col._ignore_name = True
    for col in other.columns:
      col._ignore_name = True
    ret = self.columns == other.columns
    for col in self.columns:
      col._ignore_name = False
    for col in other.columns:
      col._ignore_name = False
    return ret

  def _extra_deps (self):
    return {col for col in self.columns if col.hidden}

  def dependencies_with (self, integrity):
    deps = super().dependencies_with(integrity)
    if integrity == Reference.AUTODROP:
      deps |= {subdep for dep in self._extra_deps()
               if hasattr(dep, 'expression')
               for subdep in dep.expression.references if subdep != self}
    return deps

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
      parts.extend(self.index_properties_sql())
    except Exception as e:
      import pdb
      pdb.set_trace()
      self.log.error(
        "Index {} has columns {} had the problem {}".format(self.pretty_name,
                                                            self.columns, e))

    return " ".join(parts)

  def index_properties_sql (self):
    parts = []
    if ('index_type' in self.props and
        self.props['index_type'].endswith('/REV')):
      parts.append('REVERSE')
    if self.props['tablespace_name']:
      parts.append('TABLESPACE')
      parts.append(self.props['tablespace_name'].lower())
    return parts

  def rebuild (self):
    return [Diff("ALTER INDEX {} REBUILD".format(self.name.lower()),
                 produces=self)]

  def diff (self, other):
    prop_diffs = self._diff_props(other)
    if len(prop_diffs) == 1 and 'tablespace_name' in prop_diffs:
      return [Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
                   .format(other.name.lower(),
                           self.props['tablespace_name'].lower()),
                   produces=self)]
    else:
      return super().diff(other)

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
