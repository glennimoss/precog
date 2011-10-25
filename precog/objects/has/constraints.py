from precog.objects.constraint import Constraint, UniqueConstraint
from precog.objects.has.prop import HasProp

class HasConstraints (HasProp('constraints', assert_collection=set,
                              assert_type=Constraint)):

  @property
  def other_constraints (self):
    if not self.constraints:
      return set()
    return {cons for cons in self.constraints
            if not isinstance(cons, UniqueConstraint)}

  @property
  def unique_constraints (self):
    if not self.constraints:
      return set()
    return {cons for cons in self.constraints
            if isinstance(cons, UniqueConstraint)}

  def _eq_constraints (self, other):
    mycons = {c.name for c in self.constraints}
    othercons = {c.name for c in other.constraints}

    return mycons == othercons
