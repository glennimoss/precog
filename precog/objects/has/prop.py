from precog.objects._assert import *
from precog.objects.base import OracleObject

def HasProp (prop_name, dependency=None, assert_collection=None,
             assert_type=None):
  under_prop = '_' + prop_name
  eq_prop = '_eq_' + prop_name

  class HasProp (object):
    def __init__ (self, name, **props):
      prop_value = props.pop(prop_name)
      setattr(self, under_prop,
              assert_collection() if assert_collection else None)
      super().__init__(name, **props)
      if prop_value is not None:
        setattr(self, prop_name, prop_value)

    __hash__ = OracleObject.__hash__

    def __eq__ (self, other):
      if not super().__eq__(other):
        return False

      if not hasattr(other, prop_name):
        return False

      return getattr(self, eq_prop)(other)

    def __repr__ (self, **other_props):
      other_props[prop_name] = getattr(self, prop_name)
      return super().__repr__(**other_props)

    def satisfy (self, other):
      if self.deferred:
        super().satisfy(other)
        setattr(self, prop_name, getattr(other, prop_name))

  def eq (self, other):
    return getattr(self, prop_name) == getattr(other, prop_name)
  eq.__name__ = eq_prop
  setattr(HasProp, eq_prop, eq)

  def getter (self):
    return getattr(self, under_prop)

  def setter (self, value):
    if assert_collection or assert_type:
      _assert_type(value, assert_collection or assert_type)

    if assert_collection and assert_type:
      _assert_contains_type(value, assert_type)

    if dependency is not None:
      self._depends_on(value, under_prop, dependency)
    else:
      setattr(self, under_prop, value)

  docstring = "Property {}.".format(prop_name)
  if assert_collection or assert_type:
    docstring += ' Must be a '
    if assert_collection:
      docstring += assert_collection.__name__
    if assert_collection and assert_type:
      docstring += ' of '
    if assert_type:
      docstring += assert_type.__name__
    docstring += '.'

  setattr(HasProp, prop_name, property(getter, setter, doc=docstring))

  HasProp.__name__ += "({!r})".format(prop_name)
  return HasProp
