from precog import db
from precog.diff import Diff
from precog.objects.base import OracleObject, OracleFQN
from precog.util import InsensitiveDict

class Sequence (OracleObject):

  def __init__ (self, name, start_with=None, **props):
    super().__init__(name, **props)
    self.start_with = start_with

  def _sql (self, fq=True, operation='CREATE', props=None):
    name = self.name.obj
    if fq:
      name = self.name

    if props:
      props = InsensitiveDict({prop: expected
                               for prop, (expected, _) in props.items()})
    else:
      props = self.props

    parts = ["{} SEQUENCE {}".format(operation, name.lower())]
    if props['increment_by']:
      parts.append("INCREMENT BY {}".format(props['increment_by']))
    if props['maxvalue']:
      parts.append("MAXVALUE {}".format(props['maxvalue']))
    if props['minvalue']:
      parts.append("MINVALUE {}".format(props['minvalue']))
    if props['cycle_flag']:
      parts.append("{}CYCLE".format(
        'NO' if props['cycle_flag'] == 'N' else ''))
    if props['cache_size']:
      parts.append("CACHE {}".format(props['cache_size']))
    if props['order_flag']:
      parts.append("{}ORDER".format(
        'NO' if props['order_flag'] == 'N' else ''))

    if 'CREATE' == operation and self.start_with:
      # START WITH only applies on creation, and can't be validated after.
      parts.append("START WITH {}".format(self.start_with))

    return ' '.join(parts)

  def diff (self, other, **kwargs):
    diffs = super().diff(other, recreate=False, **kwargs)

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff(self._sql(operation='ALTER', props=prop_diff),
        produces=self, priority=Diff.ALTER))

    return diffs

  @classmethod
  def from_db (class_, schema, into_database, sequence_names=None):
    sequence_filter = db.filter_clause('sequence_name', sequence_names)
    into_database.log.debug("Querying for sequences {} from DB...".format(
      "(all)" if sequence_names is None else ", ".join(sequence_names)))
    rs = db.query(""" SELECT sequence_name
                           , min_value
                           , max_value
                           , increment_by
                           , cycle_flag
                           , order_flag
                           , cache_size
                      FROM dba_sequences
                      WHERE sequence_owner = :o
                         {}
                  """.format(sequence_filter), o=schema,
                  oracle_names=['sequence_name', 'table_owner', 'table_name'])
    into_database.log.debug("Cursor obtained")
    for row in rs:
      into_database.log.debug("Processing sequence {}".format(row['sequence_name']))
      yield class_(OracleFQN(schema, row.pop('sequence_name')),
                   database=into_database, create_location=(db.location,),
                  **row)
    rs.close()
