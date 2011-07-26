from collections import OrderedDict

class InsensitiveDict (OrderedDict):

  def __setitem__ (self, key, value):
    if isinstance(key, str):
      key = key.upper()

    super().__setitem__(key, value)

  def __getitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    try:
      return super().__getitem__(key)
    except KeyError:
      return None

  def __delitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    super().__delitem__(key)

  def __contains__ (self, key):
    if isinstance(key, str):
      key = key.upper()

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
