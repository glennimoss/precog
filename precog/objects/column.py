from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.constraint import Constraint, CheckConstraint
from precog.objects.has.constraints import HasConstraints
from precog.objects.has.expression import (HasDataDefault,
                                           HasExpressionWithDataDefault)
from precog.objects.has.prop import HasProp
from precog.objects.has.user_type import HasUserType
from precog.objects.plsql import Type

class _HasTable (HasProp('table', dependency=Reference.AUTODROP)):

  def _eq_table (self, other):
    return ((not self.table and not other.table) or
            (self.table and other.table and
             self.table.name == other.table.name))

class Column (HasConstraints, HasDataDefault, _HasTable, HasUserType,
              HasProp('qualified_col_name', assert_type=str), OracleObject):

  def __new__ (class_, *args, **props):
    # Sometimes columns are marked as virtual columns, but because they
    # represent object columns, they're also virtual.
    # We don't consider these VirtualColumns
    # Or maybe none of that is true... :P
    #if ('virtual_column' in props and 'YES' == props['virtual_column'] and
        #(('expression' in props and props['expression']) or
        #('data_default' in props and props['data_default']))):
    if 'virtual_column' in props and 'YES' == props['virtual_column']:
      class_ = VirtualColumn
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    if name.part.parts:
      props['qualified_col_name'] = name.part
      name = OracleFQN(name.schema, name.obj, GeneratedId())
    super().__init__(name, **props)
    if not self.qualified_col_name:
      self.qualified_col_name = self.name.part

  @property
  def hidden (self):
    return self.props['hidden_column'] == 'YES'

  @_HasTable.table.setter
  def table (self, value):
    _HasTable.table.__set__(self, value)
    if value:
      self.name = OracleFQN(value.name.schema, value.name.obj, self.name.part)

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
            cons.expression.text == "{} IS NOT NULL"
              .format(self.name.part.force_quoted())):
          # Get rid of the system generated constraint for NOT NULL
          not_null.add(cons)
        else:
          cons.columns = [self]
      value.difference_update(not_null)

    HasConstraints.constraints.__set__(self, value)

  @property
  def qualified_name (self):
    if self.qualified_col_name:
      return OracleFQN(self.name.schema, self.name.obj, self.qualified_col_name)
    return self.name

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

      #for cons in self.other_constraints:
      for cons in self.constraints:
        parts.append(cons.sql(inline=True))

    return " ".join(parts)

  @property
  def sql_produces (self):
    return {product for cons in self.constraints
            for product in cons.sql_produces} | {self}

  def create (self):
    diffs = [Diff("ALTER TABLE {} ADD ( {} )".format(self.table.name.lower(),
                                                     self.sql()),
                  produces=self.sql_produces, priority=Diff.CREATE)]
    #diffs.extend(diff for cons in self.unique_constraints
                 #for diff in cons.create())
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
      #rebuild = False
      #rs = db.query("""SELECT MAX(LENGTH({})) AS max_data_length
                       #FROM {}
                       #""".format(other.name.part, other.table.name))
      #max_data_length = rs[0]['max_data_length']
      #for prop, expected in prop_diff.items():
        #if 'data_type' == prop:
          #rebuild = True
          #if expected == 'NVARCHAR2':
            #if other.props['data_type'] == 'VARCHAR2'):
        #elif 'data_length' == prop:
          #if max_data_length is not None and max_data_length > expected:
            #raise DataConflict(self,
              #"has length too small for data found. (Max length {})"
                               #.format(max_data_length))
        #elif 'data_precision' == prop:
          #if expected < other.props['data_precision']:
            #rebuild = True
          #pass
        #elif 'data_scale' == prop:
          #rebuild = True
          #pass
        #elif 'char_length' == prop:
          #pass
        #elif 'char_used' == prop:
          #pass
        #elif 'nullable' == prop:
          #pass
        #elif 'virtual_column' == prop:
          #pass
        #elif 'hidden_column' == prop:
          #pass

      #if rebuild:
        #diffs.extend(self.teardown())

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

    def construct (row):
      (_, col_name), *props = row.items()

      generated = row['hidden_column'] == 'YES'
      if col_name == row['qualified_col_name']:
        row['qualified_col_name']._generated = generated
      col_name._generated = generated
      fqn = OracleFQN(name.schema, name.obj, col_name)

      props = dict(props)
      if props['data_type_owner']:
        props['user_type'] = into_database.find(
          OracleFQN(props['data_type_owner'], props['data_type']), Type)
        del props['data_type_owner']

      constraints = Constraint.from_db(OracleFQN(name.schema, name.obj,
                                                 props['qualified_col_name']),
                                       into_database)

      return class_(fqn, constraints=constraints, database=into_database,
                    **props)

    if not rs:
      into_database.log.warn("Columns not found for {}".format(name))
    return [construct(row) for row in rs]

class VirtualColumn (HasExpressionWithDataDefault, Column):
  namespace = Column

  def __init__ (self, name, **props):
    super().__init__(name, **props)

    self.props['virtual_column'] = 'YES'

  @HasExpressionWithDataDefault.expression.setter
  def expression (self, value):
    HasExpressionWithDataDefault.expression.__set__(self, value)
    if self.expression.scope_obj:
      self.table = self.expression.scope_obj

  def _sql (self, fq=False, full_def=True):
    parts = []

    if not self.hidden:
      name = self.name if fq else self.name.part
      parts.append(name.lower())

      if full_def:
        parts.append('AS (')

    if full_def or self.hidden:
      parts.append(self.expression.text)

    if full_def:
      if not self.hidden:
        parts.append(')')

      for cons in self.constraints:
        parts.append(cons.sql(inline=True))

    return " ".join(parts)
