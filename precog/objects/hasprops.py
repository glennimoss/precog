from precog.diff import Reference
from precog.objects._assert import *
from precog.objects.base import OracleObject

def HasProp (prop_name, dependency=None, assert_collection=None,
             assert_type=None):
  under_prop = '_' + prop_name
  eq_prop = '_eq_' + prop_name

  class HasProp (object):
    def __init__ (self, name, **props):
      prop_value = props.pop(prop_name)
      setattr(self, under_prop, None)
      super().__init__(name, **props)
      setattr(self, prop_name, prop_value)

    __hash__ = OracleObject.__hash__

    def __eq__ (self, other):
      if not super().__eq__(other):
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

class HasColumns (object):
  """ Mixin for objects that have the columns property """

  def __init__ (self, name, columns=[], column_reference=Reference.AUTODROP,
      **props):
    self._column_reference = column_reference
    self._columns = []
    super().__init__(name, **props)
    self.columns = columns

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycols = {c.name: c for c in self.columns}
    othercols = {c.name: c for c in other.columns}

    return mycols == othercols

  def __repr__ (self, **other_props):
    other_props['columns'] = self.columns
    return super().__repr__(**other_props)

  @property
  def columns (self):
    return self._columns

  @columns.setter
  def columns (self, value):
    _assert_type(value, list)
    _assert_contains_type(value, Column)
    if self._column_reference:
      self._depends_on(value, '_columns', self._column_reference)
    else:
      self._columns = value

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.columns = other.columns

class HasTable (object):
  """ Mixin for objects that have the table property """

  def __init__ (self, name, table=None, **props):
    self._table = None
    super().__init__(name, **props)

    self.table = table

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False
    return ((not self.table and not other.table) or
            (self.table and other.table and
             self.table.name == other.table.name))

  @property
  def table (self):
    return self._table

  @table.setter
  def table (self, value):
    _assert_type(value, Table)
    self._depends_on(value, '_table', Reference.AUTODROP)

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.table = other.table

class HasUserType (object):

  def __init__ (self, name, user_type=None, **props):
    self._user_type = None
    super().__init__(name, **props)
    self.user_type = user_type

  #_user_type = _in_props('user_type')

  @property
  def user_type (self):
    return self._user_type

  @user_type.setter
  def user_type (self, value):
    _assert_type(value, Type)
    self._depends_on(value, '_user_type')

#HasUserType = HasProp('user_type', assert_type=Type)

class HasConstraints (object):

  def __init__ (self, name, constraints=None, **props):
    self._constraints = set()
    super().__init__(name, **props)
    if constraints:
      self.constraints = constraints

  @property
  def constraints (self):
    return self._constraints

  @constraints.setter
  def constraints (self, value):
    _assert_type(value, set)
    _assert_contains_type(value, Constraint)
    self._constraints = value

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

  __hash__ = OracleObject.__hash__

  def __eq__ (self, other):
    if not super().__eq__(other):
      return False

    mycons = {c.name for c in self.constraints}
    othercons = {c.name for c in other.constraints}

    return mycons == othercons

  def __repr__ (self, **other_props):
    other_props['constraints'] = self.constraints
    return super().__repr__(**other_props)

  def satisfy (self, other):
    if self.deferred:
      super().satisfy(other)
      self.constraints = other.constraints


