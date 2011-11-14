import re

from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.constraint import (Constraint, CheckConstraint,
                                       UniqueConstraint)
from precog.objects.has.constraints import HasConstraints
from precog.objects.has.expression import (HasDataDefault,
                                           HasExpressionWithDataDefault)
from precog.objects.has.prop import HasProp
from precog.objects.has.user_type import HasUserType
from precog.objects.index import Index
from precog.objects.plsql import Type

_is_char = re.compile('(VAR)?CHAR', re.I)
_is_nchar = re.compile('N(VAR)?CHAR', re.I)
_valid_string_type = re.compile('^(N)?(VAR)?CHAR(2)?$', re.I)
_is_string_type = lambda data_type: _valid_string_type.match(data_type)
_is_number_type = lambda data_type: data_type in ('NUMBER', 'FLOAT')

class _HasTable (HasProp('table', dependency=Reference.AUTODROP)):

  def _eq_table (self, other):
    return ((not self.table and not other.table) or
            (self.table and other.table and
             self.table.name == other.table.name))

class Column (HasConstraints, HasDataDefault, _HasTable,
              HasUserType, HasProp('qualified_col_name', assert_type=str),
              OracleObject):

  def __new__ (class_, *args, **props):
    # Sometimes columns are marked as virtual columns, but because they
    # represent object columns, they're also virtual.
    # We don't consider these VirtualColumns
    if ('virtual_column' in props and 'YES' == props['virtual_column'] and
        (('expression' in props and props['expression']) or
        ('data_default' in props and props['data_default']))):
      class_ = VirtualColumn
    return super().__new__(class_, *args, **props)

  def __init__ (self, name, internal_column_id=None, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(part=name)
    if name.part.parts:
      props['qualified_col_name'] = name.part
      name = OracleFQN(name.schema, name.obj, GeneratedId())
    super().__init__(name, **props)
    if not self.qualified_col_name:
      self.qualified_col_name = self.name.part
    self.internal_column_id = internal_column_id

  @property
  def hidden (self):
    return self.props['hidden_column'] == 'YES'

  @_HasTable.table.getter
  def table (self):
    table = _HasTable.table.__get__(self)
    if not table:
      from precog.objects.table import Table
      table = self.database.find(self.name.without_part(), Table)
      self.table = table
    return table

  @HasUserType.user_type.setter
  def user_type (self, value):
    HasUserType.user_type.__set__(self, value)
    if value:
      self.props['data_type'] = value.name.lower()

  @HasConstraints.constraints.getter
  def constraints (self):
    constraints = set()
    for cons in self._constraints:
      if not (isinstance(cons, CheckConstraint) and
              cons.name.generated and
              self.props['nullable'] == 'N' and
              cons.expression.text == "{} IS NOT NULL"
              .format(self.name.part.force_quoted())):
        # Add any except system generated constraint for NOT NULL
        constraints.add(cons)
    return constraints

  @property
  def qualified_name (self):
    if self.qualified_col_name:
      return OracleFQN(self.name.schema, self.name.obj, self.qualified_col_name)
    return self.name

  @property
  def _is_pk (self):
    for ref in self._referenced_by:
      if isinstance(ref.from_, UniqueConstraint) and ref.from_.is_pk:
        return True
    return False

  def _sql (self, fq=False, full_def=True, default_clause=True):
    parts = []
    name = self.qualified_name
    if not fq:
      name = name.part
    parts.append(name.lower())

    if full_def:
      parts.append(self._data_type_sql())

      if default_clause and self.data_default:
        parts.append("DEFAULT {}".format(self.data_default))

      if self.props['nullable'] and not self._is_pk:
        if 'N' == self.props['nullable']:
          parts.append('NOT')
        parts.append('NULL')

      #for cons in self.other_constraints:
      for cons in self.constraints:
        parts.append(cons.sql(inline=True))

    return " ".join(parts)


  def _data_type_sql (self):
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
    return data_type

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

  def _diff_props (self, other):
    prop_diff = super()._diff_props(other)
    if self._is_pk and 'nullable' in prop_diff:
      del prop_diff['nullable']
    return prop_diff

  def diff (self, other, **kwargs):
    #if self.name == 'GIM.ADMIN_VERTICAL.NAME':
      #import pdb
      #pdb.set_trace()
    diffs = super().diff(other, recreate=False, **kwargs)

    prop_diff = self._diff_props(other)
    if 'constraints' in prop_diff:
      del prop_diff['constraints']

    if prop_diff:
      teardown = False
      #if (self.database.find(lambda o: o.table.name == self.table.name and
                            #self in o.columns, Constraint) or
          #self.database.find(lambda o: self in o.columns, Index)):
        #teardown = True
      recreate = False
      copypasta = False
      data_type_change = False
      nullable = None
      data_default_change = False

      max_data_length = None
      max_data_precision = None
      max_data_scale = None
      other_data_type = other.props['data_type']
      if (('data_type' in prop_diff or 'data_length' in prop_diff) and
          _is_string_type(other_data_type)):
        max_data_length = db.query_one(""" SELECT MAX(LENGTH({})) AS max
                                           FROM {}
                                       """.format(other.name.part,
                                                  other.table.name))['max']
      elif (('data_precision' in prop_diff or 'data_scale' in prop_diff) and
            _is_number_type(other_data_type)):
        rs = db.query_one(""" SELECT MAX(LENGTH(TRUNC(ABS({0}))))
                                       AS max_data_precision
                                   , MAX(LENGTH(ABS({0} - TRUNC({0}))) - 1)
                                       AS max_data_scale
                              FROM {1}
                          """.format(other.name.part, other.table.name))
        max_data_precision = rs['max_data_precision']
        max_data_scale = rs['max_data_scale']
      for prop, expected in prop_diff.items():
        other_prop = other.props[prop]
        if 'data_type' == prop:
          data_type_change = True
          if (max_data_length and
              not (_is_char.match(other_prop) and
                   _is_nchar.match(expected))):
            copypasta = True
        elif prop in ('data_length', 'char_length'):
          data_type_change = True
          if max_data_length is not None and max_data_length > expected:
            raise DataConflict(self,
              "has length too small for data found. (Min length {})"
                               .format(max_data_length))
        elif 'data_precision' == prop:
          data_type_change = True
          if max_data_precision:
            if max_data_precision > expected:
              raise DataConflict(self,
                "has precision too small for data found. (Min precision {})"
                                 .format(max_data_precision))

            if expected < other_prop:
              copypasta = True
        elif 'data_scale' == prop:
          if max_data_scale:
            copypasta = True
            if max_data_scale > expected:
              raise DataConflict(self,
                "has scale too small for data found. (Min scale {})"
                                 .format(max_data_scale))
          data_type_change = True
        elif 'char_used' == prop:
          data_type_change = True
        elif 'nullable' == prop:
          nullable = expected == 'Y'
        elif 'virtual_column' == prop:
          self.log.warn("{} is changing virtual_column from {} to {}".format(
            other.pretty_name, other_prop, expected))
          recreate = True
        elif 'hidden_column' == prop:
          self.log.warn("{} is changing hidden_column from {} to {}".format(
            other.pretty_name, other_prop, expected))
          recreate = True
        elif ('data_default' == prop and
              (expected or other_prop.upper() != 'NULL')):
          if isinstance(self, VirtualColumn):
            data_type_change = True
          else:
            data_default_change = True
        elif 'expression' == prop:
          data_type_change = True

      modify_clauses = []
      if data_type_change:
        # Data type must always come directly after the name
        modify_clauses.append(self._data_type_sql())

      if data_default_change:
        modify_clauses.append(
          "DEFAULT {}".format(self.data_default or 'NULL'))

      if nullable is not None and not self._is_pk:
        if not nullable:
          modify_clauses.append('NOT')
        modify_clauses.append('NULL')

      if recreate:
        diffs.extend(self.recreate(other))
      elif modify_clauses:
        diffs.append(Diff("ALTER TABLE {} MODIFY ( {} {} )"
                          .format(other.table.name.lower(),
                                  self._sql(full_def=False),
                                  " ".join(modify_clauses)),
                                  produces=self))

    return diffs

  @classmethod
  def from_db (class_, schema, into_database):
    rs = db.query(""" SELECT table_name
                           , column_name
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
                           , internal_column_id
                           , CURSOR(
                               SELECT constraint_name
                               FROM dba_cons_columns dcc
                               WHERE dcc.owner = dtc.owner
                                 AND dcc.table_name = dtc.table_name
                               GROUP BY constraint_name
                               HAVING COUNT(*) = 1
                                  AND MAX(column_name) = dtc.column_name
                             ) AS constraints
                      FROM dba_tab_cols dtc
                      WHERE owner = :o
                  """, o=schema, oracle_names=['table_name', 'column_name',
                                               'qualified_col_name',
                                               'constraint_name',
                                               'data_type_owner', 'data_type'])
    for row in rs:
      (_, table_name), (_, col_name), *props, (_, constraints) = row.items()
      props = dict(props)

      generated = props['hidden_column'] == 'YES'
      if col_name == props['qualified_col_name']:
        props['qualified_col_name']._generated = generated
      col_name._generated = generated
      column_name = OracleFQN(schema, table_name, col_name)

      if props['data_type_owner']:
        props['user_type'] = into_database.find(
          OracleFQN(props['data_type_owner'], props['data_type']), Type)
        del props['data_type_owner']
      else:
        # Remove quotes that may be on built-in types
        props['data_type'] = props['data_type'].strip('"')

      constraints = {
        into_database.find(OracleFQN(schema, cons['constraint_name']),
                           Constraint)
        for cons in constraints}

      yield class_(column_name, constraints=constraints,
                    database=into_database, create_location=(db.location,),
                    **props)
    rs.close()


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
    if not self.hidden:
      return super()._sql(fq=fq, full_def=full_def, default_clause=False)

    return self.expression.text

  def _data_type_sql (self):
    return "AS ( {} )".format(self.expression.text)
