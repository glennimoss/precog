from precog.objects.base import OracleObject

class Sequence (OracleObject):

  def __init__ (self, name, start_with=None, **props):
    super().__init__(name, **props)
    self.start_with = start_with

  def _sql (self, fq=True, operation='CREATE', props=None):
    name = self.name.obj
    if fq:
      name = self.name

    if not props:
      props = self.props

    parts = ["{} SEQUENCE {}".format(operation, name.lower())]
    if self.props['increment_by']:
      parts.append("INCREMENT BY {}".format(self.props['increment_by']))
    if self.props['maxvalue']:
      parts.append("MAXVALUE {}".format(self.props['maxvalue']))
    if self.props['minvalue']:
      parts.append("MINVALUE {}".format(self.props['minvalue']))
    if self.props['cycle_flag']:
      parts.append("{}CYCLE".format(
        'NO' if self.props['cycle_flag'] == 'N' else ''))
    if self.props['cache_size']:
      parts.append("CACHE {}".format(self.props['cache_size']))
    if self.props['order_flag']:
      parts.append("{}ORDER".format(
        'NO' if self.props['order_flag'] == 'N' else ''))

    if 'CREATE' == operation and self.start_with:
      # START WITH only applies on creation, and can't be validated after.
      parts.append("START WITH {}".format(self.start_with))

    return ' '.join(parts)

  def diff (self, other):
    diffs = super().diff(other, False)

    prop_diff = self._diff_props(other)
    if prop_diff:
      diffs.append(Diff(self._sql(operation='ALTER', props=prop_diff),
        produces=self, priority=Diff.ALTER))

    return diffs

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT min_value
                           , max_value
                           , increment_by
                           , cycle_flag
                           , order_flag
                           , cache_size
                      FROM dba_sequences
                      WHERE sequence_owner = :o
                        AND sequence_name = :n
                  """, o=name.schema, n=name.obj)
    if not rs:
      return None
    return class_(name, database=into_database, **rs[0])
