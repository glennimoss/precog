__all__ = ['_type_to_class_name']

def _type_to_class_name (type):
  return ''.join(word.capitalize() for word in type.split())
