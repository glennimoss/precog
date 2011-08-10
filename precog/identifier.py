import re

from precog import reserved
from precog.errors import *
from precog.util import coerced_comparison

@coerced_comparison
class OracleIdentifier (str):

  @staticmethod
  def has_parts (name):
    return bool(re.match(r'^"[^"]+"(\."[^"]+")+$', name))

  def __new__ (self, identifier):
    if isinstance(identifier, OracleIdentifier):
      return identifier

    if OracleIdentifier.has_parts(identifier):
      # Sometimes names can have multiple dotted parts. This is for object
      # columns and is probably only coming from oracle, so we'll trust it.
      pass
    else:
      identifier = str(identifier)
      quoted = identifier.startswith('"') and identifier.endswith('"')
      if not quoted:
        identifier = identifier.upper()

      if len(identifier) == (0 if not quoted else 2):
        raise OracleNameError("Object name cannot be empty")

      if identifier in reserved.words:
        raise ReservedNameError(
          "Object name {} is a reserved word".format(repr(identifier)))

      if len(identifier) > (30 if not quoted else 32):
        raise OracleNameError(
          "Object name {} is longer than 30 characters"
          .format(repr(identifier)))

      if (not quoted and
          not re.match('^[A-Z_$#][0-9A-Z_$#]*$', identifier)):
        raise OracleNameError(
          "Object name {} must not start with a number and "
          "otherwise contain only letters, numbers, _, $, or #"
          .format(repr(identifier)))

      if (quoted and
          not re.match('^"[^"\0]+"$', identifier)):
        raise OracleNameError(
          "Quoted object name {} cannot contain \" or \\0"
          .format(repr(identifier)))

    return super().__new__(self, identifier)

  def __repr__ (self):
    return "OracleIdentifier({})".format(super().__repr__())

class OracleFQN (object):
  """
  Create a fully-qualified Oracle identifier. If from_oracle is True, it will
  try to guess if the name should be quoted.
  """
  def __init__ (self, schema=None, obj=None, part=None, from_oracle=False):
    make_name = OracleIdentifier
    if from_oracle:
      make_name = name_from_oracle

    self._schema = make_name(schema) if schema else None
    self._obj = make_name(obj) if obj else None
    self._part = make_name(part) if part else None

    if not (self.schema or self.obj or self.part):
      raise OracleNameError('have to have a name')

  @property
  def schema (self):
    return self._schema

  @property
  def obj (self):
    return self._obj

  @property
  def part (self):
    return self._part

  def __str__ (self):
    return '.'.join(x for x in (self.schema, self.obj, self.part) if x)

  def __repr__ (self):
    return "OracleFQN({})".format(', '.join(
        "{}='{}'".format(arg, val) for arg, val in
          (('schema', self.schema), ('obj', self.obj), ('part', self.part))
          if val))

  def __hash__ (self):
    return self.__str__().__hash__()

  def __eq__ (self, other):
    if not isinstance(other, OracleFQN):
      return False

    return (self.schema == other.schema and
            self.obj == other.obj and
            self.part == other.part)

def name_from_oracle (name):
  if not name:
    return name

  # Sometimes the name has multiple parts, so we'll try and use it as-is.
  if OracleIdentifier.has_parts(name):
    return OracleIdentifier(name)

  if name.upper() == name:
    try:
      return OracleIdentifier(name)
    except ReservedNameError:
      # built-in types will just be strings
      return name
    except OracleNameError:
      pass

  return OracleIdentifier('"{}"'.format(name))
