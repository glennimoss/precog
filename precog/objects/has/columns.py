from precog.diff import Reference
from precog.identifier import OracleIdentifier
from precog.objects.has.prop import HasProp

class HasColumns (HasProp('columns', dependency=Reference.AUTODROP,
                          assert_collection=list)):

  def _eq_columns (self, other):
    names = lambda cols: {c.name for c in cols}
    return names(self.columns) == names(other.columns)


_OwnsColumns = HasProp('columns', assert_collection=list)
class OwnsColumns (_OwnsColumns):

  def _eq_columns (self, other):
    mycols = {col for col in self.columns if not col.hidden}
    othercols = {col for col in other.columns if not col.hidden}
    return mycols == othercols

  def _diff_props (self, other):
    return super(_OwnsColumns, self)._diff_props(other)

class HasTableFromColumns (object):

  @property
  def table (self):
    if self.columns:
      table = self.columns[0].table
      if table:
        return table
    return None
