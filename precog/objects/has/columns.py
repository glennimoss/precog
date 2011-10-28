from precog.diff import Reference
from precog.identifier import OracleIdentifier
from precog.objects.has.prop import HasProp

def _HasColumns (column_reference):
  # Can't assert type of Column because of circular dependency
  class HasColumns (HasProp('columns', dependency=column_reference,
                            assert_collection=list)):

    def _eq_columns (self, other):
      mycols = {c.name for c in self.columns}
      othercols = {c.name for c in other.columns}

      return mycols == othercols

  return HasColumns

HasColumns = _HasColumns(Reference.AUTODROP)
OwnsColumns = _HasColumns(None)

class HasTableFromColumns (object):

  @property
  def table (self):
    col_name = ''
    if self.columns:
      table = self.columns[0].table
      if table:
        return table
      col_name = " ON {}".format(self.columns[0].name)
    from precog.objects.table import Table
    return Table(OracleIdentifier('"NONEXISTENT TABLE{}"'.format(col_name),
                                  trust_me=True), deferred=True)
