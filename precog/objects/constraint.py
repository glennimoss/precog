from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects._assert import _assert_type
from precog.objects.base import OracleObject
from precog.objects.has.columns import HasColumns, HasTableFromColumns
from precog.objects.has.expression import HasExpression
from precog.objects.has.prop import HasProp
from precog.objects.index import Index

class Constraint (HasProp('is_enabled', assert_type=bool), HasTableFromColumns,
                  HasColumns, OracleObject):

  def _sql (self, fq=False, inline=False):
    parts = ['CONSTRAINT']
    name = self.name if fq else self.name.obj
    parts.append(name.lower())

    parts.extend(self._sub_sql(inline))

    if self.is_enabled is not None:
      parts.append('ENABLE' if self.is_enabled else 'DISABLE')

    return " ".join(parts)

  def _sub_sql (self, inline):
    return ['']

  def _column_list (self):
    return "( {} )".format(", ".join(col.sql(full_def=False)
                                     for col in self.columns))

  def create (self):
    try:
      return [Diff("ALTER TABLE {} ADD {}"
                   .format(self.table.name.lower(), self.sql()),
                   produces=self, priority=Diff.CREATE)]
    except Exception as e:
      self.log.error("{} had this problem: {}".format(self.pretty_name, e))

  def _drop (self):
    return Diff("ALTER TABLE {} DROP CONSTRAINT {}"
                .format(self.table.name.lower(), self.name.obj.lower()),
                self, priority=Diff.DROP)

  def rename (self, other):
    return Diff("ALTER TABLE {} RENAME CONSTRAINT {} TO {}"
                .format(other.table.name.lower(), other.name.obj.lower(),
                        self.name.obj.lower()), produces=self)

  def diff (self, other):
    prop_diffs = self._diff_props(other)
    if len(prop_diffs) == 1 and 'is_enabled' in prop_diffs:
      return [Diff("ALTER TABLE {} MODIFY CONSTRAINT {} {}"
                   .format(other.table.name.lower(), self.name.obj,
                           'ENABLE' if self.is_enabled else 'DISABLE'),
                   produces=self)]
    else:
      return super().diff(other)

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT constraint_name
                           , constraint_type
                           , status
                           , generated
                           , CURSOR(
                               SELECT table_name
                                    , column_name
                               FROM dba_cons_columns dcc
                               WHERE dcc.owner = dc.owner
                                 AND dcc.constraint_name = dc.constraint_name
                               ORDER BY dcc.position
                             ) AS columns

                           -- For check constraints
                           , search_condition

                           -- For foreign key constraints
                           , r_owner
                           , r_constraint_name
                           , delete_rule

                           -- For PK/unique constraints
                           , index_owner
                           , index_name
                      FROM dba_constraints dc
                      WHERE owner = :o
                        AND (:n IS NULL OR constraint_name = :n)
                  """, o=name.schema, n=name.obj,
                  oracle_names=['constraint_name', 'r_owner',
                                'r_constraint_name', 'index_owner',
                                'index_name', 'table_name', 'column_name'])

    constraints = set()
    for row in rs:
      constraint_name = OracleFQN(name.schema,
            OracleIdentifier(row['constraint_name'], trust_me=True,
                             generated=(row['generated'] == 'GENERATED NAME')))
      type = row['constraint_type']
      constraint_class = None
      props = {}
      from precog.objects.column import Column
      columns = [into_database.find(OracleFQN(name.schema,
                                              col['table_name'],
                                              col['column_name']),
                                    Column)
                 for col in row['columns']]
      if not columns:
        # I don't think there should be constraints without columns...
        # but there seems to be...
        into_database.log.warn(
          "Constraint {} has no columns. Constraint skipped.".format(name))
        continue

      if type == 'C':
        props['expression'] = row['search_condition']
        constraint_class = CheckConstraint

      elif type in ('P', 'U'):
        props['is_pk'] = type == 'P'
        if row['index_name']:
          props['index'] = into_database.find(OracleFQN(row['index_owner'],
                                                        row['index_name']),
                                              Index)
        constraint_class = UniqueConstraint

      elif type == 'R':
        props['fk_constraint'] = into_database.find(
          OracleFQN(row['r_owner'], row['r_constraint_name']), UniqueConstraint)
        props['delete_rule'] = row['delete_rule']
        constraint_class = ForeignKeyConstraint
      else:
        raise UnimplementedFeatureError(
          "Constraint {} has unsupported type {}".format(constraint_name, type))

      constraints.add(constraint_class(constraint_name,
                                       is_enabled=(row['status'] == 'ENABLED'),
                                       database=into_database, columns=columns,
                                       create_location=(db.location,), **props))

    return constraints

class NullConstraint (Constraint):

  def _sub_sql (self, inline):
    parts = ['NULL']
    if 'N' == self.props['nullable']:
      parts.insert(0, 'NOT')
    return parts

class CheckConstraint (HasExpression, Constraint):
  namespace = Constraint

  def _sub_sql (self, inline):
    return ['CHECK (', self.expression.text, ')']

_HasIndex = HasProp('index')
class UniqueConstraint (HasProp('is_pk', assert_type=bool), _HasIndex,
                        Constraint):
  namespace = Constraint

  FULL_INDEX_CREATE = object()
  SHORT_INDEX_CREATE = object()
  IMPLICIT_INDEX_CREATE = object()

  def __init__ (self, name, index_ownership=None, **props):
    self.index_ownership = index_ownership
    super().__init__(name, **props)

  @_HasIndex.index.setter
  def index (self, value):
    _assert_type(value, Index)
    self._depends_on(value, '_index', Reference.AUTODROP
                     if self.index_ownership else Reference.HARD)
    if self.index and not self.index.columns:
      # If our index has no columns it was likely created as part of an inline
      # constraint, so once the constraint is told its columns, it should pass
      # them on to the index if it needs them.
      self.index.columns = self.columns

  def _eq_index (self, other):
    if not self.index:
      return False
    self.index._ignore_name = True
    ret = other.index and (self.index.name == other.index.name
                           or self.index == other.index)
    self.index._ignore_name = False
    return ret

  @Constraint.columns.setter
  def columns (self, value):
    Constraint.columns.__set__(self, value)
    if self.columns and self.index and not self.index.columns:
      # see above
      self.index.columns = self.columns

  def _sub_sql (self, inline):
    parts = ['PRIMARY KEY' if self.is_pk else 'UNIQUE']
    if not inline:
      parts.append(self._column_list())
    if (self.index and
        self.index_ownership is not UniqueConstraint.IMPLICIT_INDEX_CREATE):
      parts.append('USING INDEX')

      if self.index_ownership is UniqueConstraint.FULL_INDEX_CREATE:
        parts.append('(')
        parts.append(self.index.sql())
        parts.append(')')
      elif self.index_ownership is UniqueConstraint.SHORT_INDEX_CREATE:
        parts.extend(self.index.index_properties_sql())
      else:
        parts.append(self.index.name.lower())

    return parts

  @property
  def sql_produces (self):
    if self.index_ownership:
      return {self, self.index}
    return {self}

  def diff (self, other):
    if self.index_ownership is not None and other.index_ownership is None:
      # The DB doesn't have a way to query index ownership, so we'll adopt the
      # definition's setting
      other.index_ownership = self.index_ownership
    return super().diff(other)

  def _drop (self):
    diff = super()._drop()
    if self.index_ownership:
      diff.sql[0] += ' DROP INDEX'
    else:
      diff.sql[0] += ' KEEP INDEX'
    return diff

_HasFkConstraint = HasProp('fk_constraint', dependency=Reference.HARD,
                           assert_type=UniqueConstraint)
class ForeignKeyConstraint (_HasFkConstraint, HasProp('delete_rule'),
                            Constraint):
  namespace = Constraint

  def _sub_sql (self, inline):
    parts = []
    if not inline:
      parts.append('FOREIGN KEY')
      parts.append(self._column_list())

    parts.extend(['REFERENCES', self.fk_constraint.table.name.lower(),
                  self.fk_constraint._column_list()])
    if self.delete_rule and self.delete_rule != 'NO ACTION':
      parts.append('ON DELETE')
      parts.append(self.delete_rule)

    return parts
