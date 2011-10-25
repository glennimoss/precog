from precog.diff import Reference
from precog.objects.has.prop import HasProp

def _HasColumns (column_reference):
  # Can't assert type of Column because of circular dependency
  class HasColumns (HasProp('columns', dependency=column_reference,
                            assert_collection=list)):

    def _eq_columns (self, other):
      mycols = {c.name: c for c in self.columns}
      othercols = {c.name: c for c in other.columns}

      return mycols == othercols

  return HasColumns

HasColumns = _HasColumns(Reference.AUTODROP)
OwnsColumns = _HasColumns(None)
