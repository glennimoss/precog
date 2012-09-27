__all__ = ['_assert_type', '_assert_contains_type']

def _assert_type (value, type):
  if value is not None and not isinstance(value, type):
    raise TypeError("Expected {}: {!r}".format(type.__name__, value))

def _assert_contains_type (value, contains_type):
  if value is not None:
    bad = []
    for item in value:
      try:
        _assert_type(item, contains_type)
      except TypeError:
        bad.append(item)

      if bad:
        raise TypeError("In container {}: {}".format(pprint.pformat(value),
                                                     ", ".join(str(bad))))
