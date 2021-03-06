from precog.diff import Reference
from precog.objects.has.prop import HasProp

_HasColumnsProp = HasProp('columns', dependency=Reference.AUTODROP, assert_collection=list)
class _HasColumnsLogic ():
  comparable = set

  def _eq_columns (self, other):
    from precog.objects.column import VirtualColumn
    names = lambda cols: self.comparable(c if isinstance(c, VirtualColumn) else c.name
                                         for c in cols)
    return names(self.columns) == names(other.columns)

class HasColumns (_HasColumnsLogic, _HasColumnsProp):
  pass

_HasSoftColumnsProp = HasProp('columns', dependency=Reference.SOFT, assert_collection=list)
class HasSoftColumns (_HasColumnsLogic, _HasSoftColumnsProp):
  pass

class HasOrderedColumns (HasColumns):
  comparable = list

_OwnsColumns = HasProp('columns', assert_collection=list)
class OwnsColumns (_OwnsColumns):

  def _eq_columns (self, other):
    mycols = {col for col in self.columns if not col.hidden}
    othercols = {col for col in other.columns if not col.hidden}
    return mycols == othercols

  def diff (self, other, **kwargs):
    diffs = super().diff(other, **kwargs)
    diffs.extend(self.diff_subobjects(other,
                                      lambda o: [column for column in o.columns
                                                 if not column.hidden],
                                      rename=False))
    return diffs

class HasTableFromColumns (object):

  @property
  def table (self):
    if self.columns:
      table = self.columns[0].table
      if table:
        return table
    return None
