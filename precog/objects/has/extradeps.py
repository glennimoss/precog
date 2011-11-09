from precog.objects.base import OracleObject

class HasExtraDeps (object):

  def _extra_deps (self):
    return set()

  @property
  def dependencies (self):
    deps = OracleObject.dependencies.__get__(self)
    return (deps |
            {subdep for dep in self._extra_deps()
             for subdep in dep.dependencies if subdep != self})

  def dependencies_with (self, integrity):
    deps = super().dependencies_with(integrity)
    extra_deps = self._extra_deps()
    return (deps |
            {subdep for dep in extra_deps
             for subdep in dep.dependencies_with(integrity)
             if subdep not in (extra_deps | {self})})
