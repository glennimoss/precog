from collections import OrderedDict
import logging

class InsensitiveDict (OrderedDict):

  def __setitem__ (self, key, value):
    if isinstance(key, str):
      key = key.lower()

    super().__setitem__(key, value)

  def __getitem__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    try:
      return super().__getitem__(key)
    except KeyError:
      return None

  def __delitem__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    super().__delitem__(key)

  def __contains__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    return super().__contains__(key)

def coerced_comparison (class_):
  def coerced_method (m):
    def c_m (self, other):
      try:
        other = class_(other)
      except Exception:
        # Compare as-is if coercion isn't possible
        pass

      return m(self, other)

    c_m.__name__ = m.__name__
    return c_m

  for m_name in 'eq ne lt le gt ge cmp contains'.split():
    m_name = "__{}__".format(m_name)

    # Find the method that would be resolved
    for Sup in class_.__mro__:
      if m_name in Sup.__dict__:
        orig_m = getattr(Sup, m_name)
        break

    if not orig_m:
      continue

    coerced_m = coerced_method(orig_m)
    setattr(class_, m_name, coerced_m)

  return class_

class HasLog (object):
  """ Mixin for making a log named after the class """

  def __init__ (self):
    self.log = HasLog.log_for(self)

  @staticmethod
  def log_for (obj):
    id_ = ''
    if isinstance(obj, type):
      class_ = obj
    else:
      class_ = type(obj)
      id_ = ".{}".format(id(obj))

    return logging.getLogger(
        "{}.{}{}".format(class_.__module__, class_.__name__, id_))
