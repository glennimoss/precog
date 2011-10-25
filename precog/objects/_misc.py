__all__ = ['_type_to_class']

def _type_to_class (type):
  class_name = ''.join(word.capitalize() for word in type.split())
  try:
    return globals()[class_name]
  except KeyError:
    raise _UnexpectedTypeError()
