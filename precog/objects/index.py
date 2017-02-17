from precog import db
from precog.diff import Diff, Reference
from precog.identifier import OracleFQN, OracleIdentifier
from precog.objects.base import OracleObject
from precog.objects.has.columns import HasOrderedColumns, HasTableFromColumns

class Index (HasTableFromColumns, HasOrderedColumns, OracleObject):

  def __init__ (self, name, unique=None, reverse=None, **props):
    super().__init__(name, **props)
    if unique is not None:
      self.unique = unique

  @HasOrderedColumns.columns.setter
  def columns (self, value):
    HasOrderedColumns.columns.__set__(self, value)
    if (self.props['index_type'] and
        [col for col in self.columns if col.is_virtual]):
      self.props['index_type'] = "FUNCTION-BASED {}".format(
        self.props['index_type'].split()[-1])

  @OracleObject.dependencies.getter
  def dependencies (self):
    deps = OracleObject.dependencies.__get__(self)
    deps |= {subdep for dep in self.columns
             if hasattr(dep, 'expression')
             for subdep in dep.expression.references if subdep != self}
    return deps

  def dependencies_with (self, integrity):
    deps = super().dependencies_with(integrity)
    if integrity == Reference.AUTODROP:
      deps |= {subdep for dep in self.columns
               if hasattr(dep, 'expression')
               for subdep in dep.expression.references if subdep != self}
    return deps

  @property
  def unique (self):
    return self.props['uniqueness'] == 'UNIQUE'

  @property
  def partitioned (self):
    return self.props['partitioned'] == 'YES'

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
      self.log.error(
        "Index {} has columns {} had the problem {}".format(self.pretty_name,
                                                            self.columns, e))

    return " ".join(parts)

  def index_properties_sql (self):
    parts = []
    if ('index_type' in self.props and
        self.props['index_type'].endswith('/REV')):
      parts.append('REVERSE')
    if self.props['tablespace_name'] and not self.partitioned:
      parts.append('TABLESPACE')
      parts.append(self.props['tablespace_name'].lower())
    return parts

  def rebuild (self):
    return [Diff("ALTER INDEX {} REBUILD".format(self.name.lower()),
                 produces=self)]

  def diff (self, other, **kwargs):
    prop_diffs = self._diff_props(other)
    if len(prop_diffs) == 1 and 'tablespace_name' in prop_diffs:
      return [Diff("ALTER INDEX {} REBUILD TABLESPACE {}"
                   .format(other.name.lower(),
                           self.props['tablespace_name'].lower()),
                   produces=self)] if not other.partitioned else []
    return super().diff(other, **kwargs)

  @classmethod
  def from_db (class_, schema, into_database, index_names=None):
    index_filter = db.filter_clause('index_name', index_names)
    rs = db.query(""" SELECT index_name
                           , index_type
                           , uniqueness
                           , tablespace_name
                           , status
                           , partitioned
                           , table_owner
                           , table_name
                           , ( SELECT CAST(COLLECT(column_name ORDER BY dic.column_position) AS gt_string_table)
                               FROM dba_ind_columns dic
                               WHERE dic.index_owner = di.owner
                                 AND dic.index_name = di.index_name
                             ) AS columns
                      FROM dba_indexes di
                      WHERE owner = :o
                         {}
                  """.format(index_filter), o=schema,
                  oracle_names=['tablespace_name', 'table_owner', 'table_name',
                                'index_name', 'columns'])

    for row in rs:
      index_name = OracleFQN(schema,
            OracleIdentifier(row['index_name'], trust_me=True,
                             generated=(row['generated'] == 'Y')))
      index_type = row['index_type']
      if index_type == 'IOT - TOP':
        into_database.log.debug(
          "Index {} is for an index-organized table. Skipping..."
          .format(index_name))
        continue

      if index_type.find('NORMAL') == -1:
        into_database.log.debug(
          "Index {} is an unsupported type {}. Skipping...".format(index_name,
                                                                  index_type))
        continue
        #raise UnimplementedFeatureError(
          #"Index {} has unsupported type {}".format(index_name, index_type))

      from precog.objects.column import Column
      columns = [into_database.find(OracleFQN(row['table_owner'], row['table_name'], column_name), Column)
                 for column_name in row['columns']]
      # An index without columns is hardly an index at all!
      if not columns:
        into_database.log.debug(
          "Index {} has no columns. Index skipped.".format(index_name))
        continue

      yield class_(index_name, columns=columns, index_type=index_type,
                   uniqueness=row['uniqueness'], status=row['status'],
                   tablespace_name=row['tablespace_name'],
                   partitioned=row['partitioned'],
                   database=into_database, create_location=(db.location,))
    rs.close()
