import os
__all__ = ['_type_to_class_name', '_with_location']

def _type_to_class_name (type):
  return ''.join(word.capitalize() for word in type.split())

def _with_location (obj):
  return ", ".join([obj.pretty_name] + obj.create_location)
