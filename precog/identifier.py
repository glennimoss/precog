import re

from precog import reserved
from precog.errors import *
from precog.util import coerced_comparison

@coerced_comparison
class OracleIdentifier (str):

  @staticmethod
  def has_parts (name):
    return bool(re.match(r'^"[^"]+"(\."[^"]+")+$', name))

  @staticmethod
  def simple_name (name):
    return bool(re.match('^[A-Z_$#][0-9A-Z_$#]*$', name.strip('"')))

  def __new__ (class_, identifier, trust_me=False):
    if isinstance(identifier, OracleIdentifier):
      return identifier

    parts = None
    if isinstance(identifier, list):
      if len(identifier) > 1:
        parts = identifier
        identifier = ".".join(OracleIdentifier(id).force_quoted()
            for id in identifier)
        trust_me = True
      else:
        identifier = identifier[0]

    if trust_me:
      # Sometimes names can violate these conditions, but whoever is creating
      # this object is sure they know what they're doing. Do you?
      pass
    else:
      identifier = str(identifier)
      quoted = identifier.startswith('"') and identifier.endswith('"')
      # Normalize names
      if quoted:
        if OracleIdentifier.simple_name(identifier):
          identifier = identifier.strip('"')
          quoted = False
      else:
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

    self = super().__new__(class_, identifier)
    self.parts = parts

    return self

  def force_quoted (self):
    return OracleIdentifier('"{}"'.format(self.strip('"')), True)

  def __repr__ (self):
    return "OracleIdentifier({})".format(super().__repr__())

class OracleFQN (OracleIdentifier):
  """
  Create a fully-qualified Oracle identifier. If from_oracle is True, it will
  try to guess if the name should be quoted.
  """
  def __new__ (class_, schema=None, obj=None, part=None, from_oracle=False):
    make_name = OracleIdentifier
    if from_oracle:
      make_name = name_from_oracle

    schema = make_name(schema) if schema else None
    obj = make_name(obj) if obj else None
    part = make_name(part) if part else None

    if not (schema or obj or part):
      raise OracleNameError('have to have a name')

    text = '.'.join(x for x in (schema, obj, part) if x)
    self = super().__new__(class_, text, True)

    self._schema = make_name(schema) if schema else None
    self._obj = make_name(obj) if obj else None
    self._part = make_name(part) if part else None

    return self

  @property
  def schema (self):
    return self._schema

  @property
  def obj (self):
    return self._obj

  @property
  def part (self):
    return self._part

  def __repr__ (self):
    return "OracleFQN({})".format(', '.join(
        "{}='{}'".format(arg, val) for arg, val in
          (('schema', self.schema), ('obj', self.obj), ('part', self.part))
          if val))

def name_from_oracle (name):
  if not name:
    return name

  if OracleIdentifier.has_parts(name):
    # Sometimes the name has multiple parts, and we want to have access to parts
    names = name.strip('"').split('"."')
    return OracleIdentifier(names, True)

  try:
    return OracleIdentifier(name)
  except ReservedNameError:
    # built-in types
    return OracleIdentifier(name, True)
  except OracleNameError:
    return OracleIdentifier('"{}"'.format(name))
