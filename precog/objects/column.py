from precog.objects.base import OracleObject
from precog.objects.hasprops import (HasConstraints, HasTable, HasUserType,
                                     HasProp)

HasDataDefault = HasProp('data_default')
class Column (HasConstraints, HasTable, HasUserType, HasDataDefault,
              OracleObject):

  def __new__ (class_, *args, **props):
    if 'virtual_column' in props and 'YES' == props['virtual_column']:
      class_ = VirtualColumn
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    super().__init__(name, **props)

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
            cons.name.generated and
            self.props['nullable'] == 'N' and
            cons.condition.text == "{} IS NOT NULL"
              .format(self.name.part.force_quoted())):
          # Get rid of the system generated constraint for NOT NULL
          not_null.add(cons)
        else:
          cons.columns = [self]
      value.difference_update(not_null)

    HasConstraints.constraints.__set__(self, value)

  @property
  def qualified_name (self):
    part = self.name.part
    if 'qualified_col_name' in self.props:
      part = self.props['qualified_col_name']
    return OracleFQN(self.name.schema, self.name.obj, part)

  #_data_default = _in_props('data_default')

  #@_data_default.setter
  HasDataDefault.data_default.setter
  def data_default (self, value):
    if value and not isinstance(value, parser.Expression):
      value = parser.Expression(value, scope_obj=self.table,
                                database=self.database)
      self._depends_on(value.references, '_default_exp_ids')
    self._data_default = value

  #@data_default.getter
  def data_default (self):
    if self._data_default and self._data_default.scope_obj is None:
      self.data_default = self._data_default.text
    return self._data_default

  @property
  def subobjects (self):
    return self.constraints

  def _sql (self, fq=False, full_def=True):
    parts = []
    name = self.qualified_name
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

      if self.data_default:
        parts.append("DEFAULT {}".format(self.data_default))

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

    if (other.data_default and
        other.data_default != 'NULL' and
        not self.data_default):
      diffs.append(Diff("ALTER TABLE {} MODIFY ( {} DEFAULT NULL)"
                        .format(other.table.name.lower(),
                                other.name.part.lower()),
                        produces=self))

    diffs.extend(self.diff_subobjects(other, lambda o: o.constraints))

    return diffs

  #def add_subobjects (self, subobjects):
    #return [Diff("ALTER TABLE {} MODIFY ({} {})"
                 #.format(self.table.name.lower(), self.name.lower(),
                         #" ".join(obj.sql(inline=True) for obj in subobjects)))]

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
                      FROM dba_tab_cols
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

      constraints = Constraint.from_db(OracleFQN(name.schema, name.obj,
                                                 props['qualified_col_name']),
                                       into_database)

      return class_(name, constraints=constraints, database=into_database,
                    **props)

    return [construct(OracleFQN(name.schema, name.obj, col_name), props)
            for (_, col_name), *props in (row.items() for row in rs)]

class VirtualColumn (Column):
  namespace = Column

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    self.props['virtual_column'] = 'YES'

  expression = Column.data_default

  def _sql (self, fq=False, full_def=True):
    parts = []
    hidden = 'YES' == self.props['hidden_column']

    if not hidden:
      name = self.name if fq else self.name.part
      parts.append(name.lower())

      if full_def:
        parts.append('AS (')

    if full_def or hidden:
      parts.append(self.expression.text)

    if not hidden and full_def:
      parts.append(')')

    return " ".join(parts)

