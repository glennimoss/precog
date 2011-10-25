from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.has.columns import HasColumns
from precog.objects.has.expression import HasExpression
from precog.objects.has.prop import HasProp
from precog.objects.index import Index

class Constraint (HasProp('is_enabled', assert_type=bool), HasColumns,
                  OracleObject):

  @property
  def table (self):
    if self.columns:
      return self.columns[0].table
    return None

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
      import pdb
      pdb.set_trace()

  def _drop (self):
    return Diff( "ALTER TABLE {} DROP CONSTRAINT {}"
                .format(self.table.name.lower(), self.name.obj.lower()),
                self, priority=Diff.DROP)

  def diff (self, other):
    diffs = super().diff(other, False)

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff("ALTER TABLE {} MODIFY {}"
                        .format(other.table.name.lower(), self.sql()),
                        produces=self))

    return diffs

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT constraint_name
                           , constraint_type
                           , status
                           , generated
                           , table_name
                           , CURSOR(
                               SELECT table_name
                                    , column_name
                               FROM dba_cons_columns acc
                               WHERE acc.owner = ac.owner
                                 AND acc.constraint_name = ac.constraint_name
                               ORDER BY acc.position
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
                      FROM dba_constraints ac
                      WHERE owner = :o
                        AND table_name = :n
                  """, o=name.schema, n=name.obj,
                  oracle_names=['constraint_name', 'r_owner',
                                'r_constraint_name', 'index_owner',
                                'index_name', 'table_name', 'column_name'])

    if not rs:
      return None
    constraints = set()
    for row in rs:
      if name.part:
        # We're looking only for inlineable constraints on a specific column
        if (len(row['columns']) > 1 or
            row['columns'][0]['column_name'] != name.part):
          continue
      elif len(row['columns']) == 1:
        # Only Constraints with multiple columns are at the Table level
        continue

      constraint_name = OracleFQN(name.schema,
            OracleIdentifier(row['constraint_name'], trust_me=True,
                             generated=(row['generated'] == 'GENERATED NAME')))
      type = row['constraint_type']
      constraint_class = None
      props = {}
      columns = None
      if len(row['columns']) > 1:
        # If there's only one column, we'll leave it up to the caller to set it
        from precog.objects.column import Column
        columns = [into_database.find(OracleFQN(name.schema,
                                                col['table_name'],
                                                col['column_name']),
                                      Column)
                   for col in row['columns']]
      if type == 'C':
        props['expression'] = row['search_condition']
        constraint_class = CheckConstraint

      elif type in ('P', 'U'):
        props['is_pk'] = type == 'P'
        props['index'] = into_database.find(OracleFQN(row['index_owner'],
                                                      row['index_name']), Index)
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
                                       **props))

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

_HasIndex = HasProp('index', dependency=Reference.HARD, assert_type=Index)
class UniqueConstraint (HasProp('is_pk', assert_type=bool), _HasIndex,
                        Constraint):
  namespace = Constraint

  @_HasIndex.index.setter
  def index (self, value):
    _HasIndex.index.__set__(self, value)
    if self.index and not self.index.columns:
      # If our index has no columns it was likely created as part of an inline
      # constraint, so once the constraint is told its columns, it should pass
      # them on to the index if it needs them.
      self.index.columns = self.columns

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
    if self.index:
      parts.append('USING INDEX')
      parts.append(self.index.name.lower())

    return parts

  def _drop (self):
    diff = super()._drop()
    diff.sql += ' KEEP INDEX'
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
