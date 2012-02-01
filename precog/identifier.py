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

  def __new__ (class_, identifier, trust_me=False, generated=False):
    if isinstance(identifier, OracleIdentifier) and not trust_me:
      return identifier

    quoted = False
    parts = None
    if isinstance(identifier, list):
      if len(identifier) > 1:
        parts = [OracleIdentifier(id, trust_me) for id in identifier]
        identifier = ".".join(part.force_quoted() for part in parts)
        quoted = True
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
    self.quoted = quoted
    self.parts = parts
    self._generated = generated

    return self

  def __hash__ (self):
    if self.generated:
      # All generated identifiers are equal, so they must have the same hash
      return 1
    return super().__hash__()

  def __eq__ (self, other):
    if isinstance(other, OracleIdentifier):
      if self.generated and other.generated:
        # We can't really say if two generated IDs aren't equal...
        return True
      if self.generated or other.generated:
        # We must do this because otherwise the hash/eq contract is violated
        return False
    return super().__eq__(other)

  def __ne__ (self, other):
    return not self == other

  @property
  def generated (self):
    return self._generated

  def lower (self):
    if self.parts:
      return ".".join(part.lower() for part in self.parts)
    if self.quoted:
      return self
    return super().lower()

  def force_quoted (self):
    return OracleIdentifier('"{}"'.format(self.strip('"')), True)

  def __repr__ (self):
    return "OracleIdentifier({}{})".format(super().__repr__(),
                                           ', generated=True' if self.generated
                                           else '')

  def __getnewargs__ (self):
    return (str(self), True)

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
      raise OracleNameError('FQN must have at least one identifier')

    text = ".".join(x for x in (schema, obj, part) if x)
    self = super().__new__(class_, text, True)

    self._schema = schema
    self._obj = obj
    self._part = part

    return self

  def __hash__ (self):
    return hash((self.schema, self.obj, self.part))

  def __eq__ (self, other):
    if isinstance(other, OracleFQN):
      # Allow comparison to succeed if some part of the name is generated...
      return (self.schema == other.schema and self.obj == other.obj and
              self.part == other.part)

    return super().__eq__(other)

  def __ne__ (self, other):
    return not self == other

  @property
  def schema (self):
    return self._schema

  @property
  def obj (self):
    return self._obj

  @property
  def part (self):
    return self._part

  def with_ (self, schema=None, obj=None, part=None):
    if schema is None:
      schema = self.schema
    if obj is None:
      obj = self.obj
    if part is None:
      part = self.part
    return OracleFQN(schema, obj, part)

  def without_part (self):
    return OracleFQN(self.schema, self.obj)

  @property
  def generated (self):
    return ((self.schema is not None and self.schema.generated) or
            (self.obj is not None and self.obj.generated) or
            (self.part is not None and self.part.generated))

  def lower (self):
    return ".".join(x.lower() for x in (self.schema, self.obj, self.part) if x)

  def __repr__ (self):
    return "OracleFQN({})".format(', '.join(
        "{}='{}'".format(arg, val) for arg, val in
          (('schema', self.schema), ('obj', self.obj), ('part', self.part),
           ('generated', self.generated if self.generated else None))
          if val))

  def __getnewargs__ (self):
    return (self._schema, self._obj, self._part, True)

_generated_id = 0
def GeneratedId ():
  global _generated_id

  name = OracleIdentifier("PRECOG_{}".format(_generated_id), generated=True)
  _generated_id += 1

  return name

def name_from_oracle (name):
  if not name or isinstance(name, OracleIdentifier):
    return name

  if OracleIdentifier.has_parts(name):
    # Sometimes the name has multiple parts, and we want to have access to parts
    names = name.strip('"').split('"."')
    return OracleIdentifier(names, True)

  try:
    return OracleIdentifier('"{}"'.format(name))
  except OracleNameError:
    # It came from oracle... it SHOULD be good :P
    return OracleIdentifier(name, True)

defines = {}
def define (var_name, value):
  defines[var_name] = OracleIdentifier(value)

_var_ref = re.compile(r'^&\s*(\w+)\.?$')
def VariableIdentifier (var_name):
  var_name = _var_ref.match(var_name).group(1)

  if var_name not in defines:
    raise UndefinedVariableError(var_name)
  return defines[var_name]

"""
class VariableIdentifier (OracleIdentifier):

  def __new__ (class_, var_name):


    self = super().__new__(class_, '&{}.'.format(var_name), True)
    self.var_name = var_name

    return self

  def resolve (self):
    return '<{}>'.format(self.var_name)

  def __getnewargs__ (self):
    return (self.var_name,)
"""
