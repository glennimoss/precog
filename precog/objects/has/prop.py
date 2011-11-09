from precog.objects._assert import *
from precog.objects.base import OracleObject

def HasProp (prop_name, dependency=None, assert_collection=None,
             assert_type=None, strict_none=False):
  under_prop = '_' + prop_name
  eq_prop = '_eq_' + prop_name

  def equal (self, other):
    if not strict_none and (getattr(self, prop_name) is None or
                            getattr(other, prop_name) is None):
      return True

    if not hasattr(other, prop_name):
      return False

    return getattr(self, eq_prop)(other)

  class HasProp (object):
    def __init__ (self, name, **props):
      setattr(self, under_prop,
              assert_collection() if assert_collection else None)
      present = False
      prop_value = None
      if prop_name in props:
        present = True
        prop_value = props.pop(prop_name)
      super().__init__(name, **props)
      if present:
        setattr(self, prop_name, prop_value)

    __hash__ = OracleObject.__hash__

    #def __eq__ (self, other):
      #if not super().__eq__(other):
        #return False

      #ret = equal(self, other)
      ##if not ret:
        ##self.log.debug(
          ##"{} == {} failed for self.{} = {!r}, other.{} = {!r}".format(
            ##self.pretty_name, other.pretty_name, prop_name,
            ##getattr(self, prop_name), prop_name, getattr(other, prop_name)))
      #return ret

    def __ne__ (self, other):
      return not self == other

    def __repr__ (self, **other_props):
      prop_value = getattr(self, prop_name)
      if not isinstance(prop_value, str):
        try:
          prop_value = type(prop_value)(obj.pretty_name for obj in prop_value)
        except TypeError:
          pass

      other_props[prop_name] = prop_value
      return super().__repr__(**other_props)

    def _diff_props (self, other):
      prop_diff = super()._diff_props(other)
      if not equal(self, other):
        prop_diff[prop_name] = getattr(self, prop_name)
        #self.log.debug("{}['{}']: expected {!r}, found {!r}".format(
          #self.pretty_name, prop_name, getattr(self, prop_name),
          #getattr(other, prop_name)))
      return prop_diff

    def _satisfy (self, other):
      super()._satisfy(other)
      setattr(self, prop_name, getattr(other, prop_name))

  def eq (self, other):
    return getattr(self, prop_name) == getattr(other, prop_name)
  eq.__name__ = eq_prop
  setattr(HasProp, eq_prop, eq)

  def getter (self):
    if not hasattr(self, under_prop):
      return None
    return getattr(self, under_prop)

  def setter (self, value):
    if assert_collection or assert_type:
      _assert_type(value, assert_collection or assert_type)

    if assert_collection and value is None:
      value = assert_collection()

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
