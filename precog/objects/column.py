import re

from precog import db
from precog.diff import Diff, Reference
from precog.errors import PropertyConflict, DataConflict
from precog.identifier import OracleFQN, GeneratedId
from precog.objects.base import OracleObject
from precog.objects.constraint import (Constraint, CheckConstraint,
                                       UniqueConstraint)
from precog.objects.has.constraints import HasConstraints
from precog.objects.has.expression import (HasDataDefault,
                                           HasExpressionWithDataDefault)
from precog.objects.has.prop import HasProp
from precog.objects.has.user_type import HasUserType
#from precog.objects.index import Index
from precog.objects.plsql import Type

_is_char = re.compile('(VAR)?CHAR', re.I)
_is_nchar = re.compile('N(VAR)?CHAR', re.I)
_valid_string_type = re.compile('^(N)?(VAR)?CHAR(2)?$', re.I)
_is_string_type = lambda data_type: _valid_string_type.match(data_type)
_is_number_type = lambda data_type: data_type in ('NUMBER', 'FLOAT')
_is_dateish_type = lambda data_type: ('DATE' == data_type or
                                      data_type.startswith('TIMESTAMP'))

class _HasTable (HasProp('table', dependency=Reference.AUTODROP)):

  def _eq_table (self, other):
    return ((not self.table and not other.table) or
            (self.table and other.table and
             self.table.name == other.table.name))

_HasQualifiedColName_ = HasProp('qualified_col_name', assert_type=str)
class _HasQualifiedColName(_HasQualifiedColName_):
  def _satisfy (self, other):
    super(_HasQualifiedColName_, self)._satisfy(other)

    if other.qualified_col_name is not None:
      # A deferred object may have a value not marked as generated because we
      # didn't know if it was at the lookup time, and when the real one arrives
      # and it IS generated, the two will not be equal. We test for equality to
      # allow for generated name matching, but then only if they actually differ
      # by text will we make a stink.
      if (self.qualified_col_name and
          self.qualified_col_name != other.qualified_col_name and
          not str.__eq__(self.qualified_col_name, other.qualified_col_name)):
        raise PropertyConflict(self, 'qualified_col_name',
                               other.qualified_col_name)
      self.qualified_col_name = other.qualified_col_name

class Column (HasConstraints, HasDataDefault, _HasTable, HasUserType,
              _HasQualifiedColName, OracleObject):

  def __new__ (class_, *args, **props):
    # Sometimes columns are marked as virtual columns, but because they
    # represent object columns, they're also virtual.
    # We don't consider these VirtualColumns
    if ('virtual_column' in props and 'YES' == props['virtual_column'] and
        (('expression' in props and props['expression']) or
        ('data_default' in props and props['data_default']))):
      class_ = VirtualColumn
    return super().__new__(class_)

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
    self.props['virtual_column'] = 'NO'

  def _satisfy (self, other):
    super()._satisfy(other)
    self.internal_column_id = other.internal_column_id

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

  @table.setter
  def table (self, value):
    _HasTable.table.__set__(self, value)
    if value:
      self.name = value.name.with_(part=self.name.part)

  @property
  def props (self):
    if self.user_type:
      self._props['data_type'] = self.user_type.name.lower()
    return self._props

  @props.setter
  def props (self, value):
    self._props = value

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
  def is_string (self):
    return (self.props['data_type'] and
            _is_string_type(self.props['data_type']) is not None)

  @property
  def is_number (self):
    return self.props['data_type'] and _is_number_type(self.props['data_type'])

  @property
  def is_datetime (self):
    return (self.props['data_type'] and
            _is_dateish_type(self.props['data_type']))

  @property
  def is_virtual (self):
    return isinstance(self, VirtualColumn)

  @property
  def _is_pk (self):
    for uk in self._find_unique_constraints():
      if uk.is_pk:
        return True
    return False

  def _find_unique_constraints (self):
    return {ref.from_ for ref in self._referenced_by
            if isinstance(ref.from_, UniqueConstraint)}

  def _sql (self, fq=False, full_def=True):
    parts = []
    name = self.qualified_name
    if not fq:
      name = name.part
    parts.append(name.lower())

    if full_def:
      parts.append(self._data_type_sql())

      parts.append(self._extra_sql())

      if self.props['nullable'] and not self._is_pk:
        if 'N' == self.props['nullable']:
          parts.append('NOT')
        parts.append('NULL')

      for cons in self.constraints:
        parts.append(cons.sql(inline=True))

    return " ".join(x for x in parts if x)


  def _data_type_sql (self):
    data_type = self.props['data_type']
    if not data_type:
      return ''
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

  def _extra_sql (self):
    if self.data_default:
      return "DEFAULT {}".format(self.data_default)

  @property
  def sql_produces (self):
    return {product for cons in self.constraints
            for product in cons.sql_produces} | {self}

  def create (self):
    return Diff("ALTER TABLE {} ADD ( {} )".format(self.table.name.lower(),
                                                   self.sql()),
                produces=self.sql_produces, priority=Diff.CREATE)

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
      if type(self) is not VirtualColumn or 'virtual_column' not in prop_diff:
        if (('data_type' in prop_diff or
             'data_length' in prop_diff or
             'char_length' in prop_diff) and
            _is_string_type(other_data_type)):
          col_expr = other.name.part
          if other_data_type == 'CHAR':
            col_expr = "RTRIM({})".format(other.name.part)
          max_data_length = db.query_one(""" SELECT MAX(LENGTH({})) AS max
                                             FROM {}
                                         """.format(col_expr,
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
      for prop, (expected, other_prop) in prop_diff.items():
        if expected is None:
          continue

        if 'data_type' == prop:
          data_type_change = True
          if not (_is_char.match(other_prop) and
                  _is_nchar.match(expected)):
            copypasta = True
        elif prop in ('data_length', 'char_length'):
          data_type_change = True
          if other_data_type == 'CHAR' and expected < other_prop:
            copypasta = True
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

            if expected < (other_prop or 38):
              copypasta = True
        elif 'data_scale' == prop:
          data_type_change = True
          if max_data_scale:
            if max_data_scale > expected:
              raise DataConflict(self,
                "has scale too small for data found. (Min scale {})"
                                 .format(max_data_scale))
          copypasta = True
        elif 'char_used' == prop:
          data_type_change = True
        elif 'nullable' == prop:
          nullable = expected == 'Y'
        elif 'virtual_column' == prop:
          if expected == 'NO':
            copypasta = True
          recreate = True
        elif 'hidden_column' == prop:
          recreate = True
        elif 'user_type' == prop:
          recreate = True
        elif ('data_default' == prop and
              (expected or (other_prop and other_prop.upper() != 'NULL'))):
          if isinstance(self, VirtualColumn):
            data_type_change = True
          else:
            data_default_change = True
        elif 'expression' == prop:
          recreate = True

      modify_diffs = []
      if copypasta:
        has_data = db.query_one(""" SELECT COUNT({}) AS has_data
                                    FROM {}
                                """.format(other.name.part,
                                           other.table.name))['has_data']
        if has_data:
          other_table_name = other.table.name.lower()
          temp_col = "{}$$".format(GeneratedId().lower())
          teardown = other.teardown()
          create = self.create()
          create.sql.insert(0, "ALTER TABLE {} RENAME COLUMN {} TO {}"
                            .format(other_table_name, other.name.part.lower(),
                                    temp_col))

          temp_col_expr = temp_col
          if other_data_type == 'CHAR':
            # Special case because of space padding
            temp_col_expr = 'RTRIM({})'.format(temp_col)

          create.sql.extend(["UPDATE {} SET {} = {}"
                            .format(other_table_name, self.name.part.lower(),
                                    temp_col_expr),
                            'COMMIT',
                            "ALTER TABLE {} DROP ({})".format(other_table_name,
                                                             temp_col)])
          creates = self.build_up()
          creates.append(create)

          for diff in creates:
            diff.add_dependencies(teardown)
          modify_diffs.extend(teardown)
          modify_diffs.extend(creates)

      if not modify_diffs:
        if recreate:
          modify_diffs.extend(self.recreate(other))
        else:
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

          if modify_clauses:
            modify_diffs.append(Diff("ALTER TABLE {} MODIFY ( {} {} )"
                                     .format(other.table.name.lower(),
                                             self._sql(full_def=False),
                                             " ".join(modify_clauses)),
                                     produces=self))
      diffs.extend(modify_diffs)

    return diffs

  @classmethod
  def from_db (class_, schema, into_database, table_names=None):
    table_filter = db.filter_clause('table_name', table_names)
    into_database.log.debug("Querying for columns {} from DB...".format(
      "(all)" if table_names is None else "in tables {}".format(", ".join(table_names))))
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
                           , ( SELECT CAST(COLLECT(constraint_name) AS gt_string_table)
                               FROM (
                                 SELECT constraint_name
                                 FROM dba_cons_columns dcc
                                 WHERE dcc.owner = dtc.owner
                                   AND dcc.table_name = dtc.table_name
                                 GROUP BY constraint_name
                                 HAVING COUNT(*) = 1
                                    AND MAX(column_name) = dtc.column_name
                               )
                             ) AS constraints
                      FROM dba_tab_cols dtc
                         , dba_objects do
                      WHERE dtc.owner = :o
                        -- Ignore columns on tables in the recyclebin
                        AND NOT (LENGTH(table_name) = 30
                             AND table_name LIKE 'BIN$%')
                        AND do.owner = dtc.owner
                        AND do.object_name = dtc.table_name
                        AND do.object_type = 'TABLE'
                         {}
                  """.format(table_filter), o=schema,
                  oracle_names=['table_name', 'column_name',
                                'qualified_col_name', 'constraints',
                                'data_type_owner', 'data_type'])
    into_database.log.debug("Cursor obtained")
    for row in rs:
      into_database.log.debug("Grabbing a column row...")
      (_, table_name), (_, col_name), *props, (_, constraints) = row.items()
      props = dict(props)

      generated = props['hidden_column'] == 'YES'
      if col_name == props['qualified_col_name']:
        props['qualified_col_name']._generated = generated
      col_name._generated = generated
      column_name = OracleFQN(schema, table_name, col_name)
      into_database.log.debug("Processing column {}".format(column_name))

      if props['data_type_owner']:
        props['user_type'] = into_database.find(
          OracleFQN(props['data_type_owner'], props['data_type']), Type)
        del props['data_type_owner']
      elif props['data_type']:
        # Remove quotes that may be on built-in types
        props['data_type'] = props['data_type'].strip('"')

      constraints = {
        into_database.find(OracleFQN(schema, constraint_name), Constraint)
        for constraint_name in constraints}

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
    if self.expression and self.expression.scope_obj:
      self.table = self.expression.scope_obj

  def _sql (self, fq=False, full_def=True):
    if not self.hidden:
      return super()._sql(fq=fq, full_def=full_def)
    return self.expression.text

  def _extra_sql (self):
    return ' '.join(('AS (', self.expression.text, ')'))
