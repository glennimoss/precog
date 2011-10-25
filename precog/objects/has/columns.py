from precog.diff import Reference
from precog.objects.column import Column
from precog.objects.has.prop import HasProp

def _HasColumns (column_reference=Reference.AUTODROP):
  class HasColumns (HasProp('columns', dependency=column_reference,
                            assert_collection=list, assert_type=Column))

    def _eq_columns (self, other):
      mycols = {c.name: c for c in self.columns}
      othercols = {c.name: c for c in other.columns}

      return mycols == othercols

  return HasColumns

HasColumns = _HasColumns()
OwnsColumns = _HasColumns(None)
