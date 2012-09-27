from precog.parser.util import format_syntax_error
from precog.util import pluralize, _with_location

class PrecogError (Exception):

  def __str__ (self):
    return "{}: {}".format(type(self).__name__, super().__str__())

class UnimplementedFeatureError (PrecogError):
  pass

class ParseError (PrecogError):

  def __init__ (self, num_errors):
    self.num_errors = num_errors

  def __str__ (self):
    return "{}{} in schema definition".format(super().__str__(),
        pluralize(self.num_errors, 'error'))

class SyntaxError (ParseError):
  def __init__ (self, title, source_name, line, column, line_text,
      explanation=''):
    self.title = title
    self.source_name = source_name
    self.line = line
    self.column = column
    self.line_text = line_text
    self.explanation = explanation

  def __str__ (self):
    return '{}{}'.format(
      super(ParseError, self).__str__(),
      format_syntax_error(self.title, self.source_name, self.line, self.column,
                          self.line_text, self.explanation))

class SqlSyntaxError (SyntaxError):
  pass

class OracleError (PrecogError):
  def __init__ (self, db_error, sql):
    self.db_error = db_error
    self.sql = sql

  def __str__ (self):
    offset = self.db_error.args[0].offset
    lines = self.sql.split('\n')
    pos = 0
    for lineno in range(len(lines)):
      linelen = len(lines[lineno]) + 1
      if pos + linelen > offset:
        break
      pos += linelen
    offset -= pos
    lineno += 1 # 1-based line numbering

    return '{}{}'.format(
      super().__str__(),
      format_syntax_error(str(self.db_error).strip(), 'SQL statement', lineno,
                          offset, self.sql))

class UnappliedDependencyError (PrecogError):
  pass

class PlsqlSyntaxError (OracleError):

  def __init__ (self, plsql_obj, errors):
    self.plsql_obj = plsql_obj
    self.errors = errors
    parts = ["{} has {} {}s".format(plsql_obj.pretty_name, len(errors),
                                    errors[0]['attribute'].lower())]
    for error_props in errors:
      line = error_props['line']
      source_line = line
      if len(plsql_obj.create_location) > 1:
        source_line += plsql_obj.create_location[1] - 1
      parts.append(str(SyntaxError(
        "PL/SQL compile {}:".format(error_props['attribute'].lower()),
        _with_location(plsql_obj, False), source_line,
        error_props['position'] - 1, plsql_obj.sql().split('\n')[line-1],
        error_props['text'])))
    super().__init__("\n".join(parts))

class ObjectError (PrecogError):

  def __init__ (self, obj):
    self.obj = obj
    super().__init__(_with_location(self.obj))

class PropertyConflict (ObjectError):

  def __init__ (self, obj, prop_name, other_value):
    super().__init__(obj)

    self.prop_name = prop_name
    self.other_value = other_value

  def __str__ (self):
    return ("{} with property {} of {} is trying to be satisfied "
            "with a different value {}".format(
              super().__str__(), self.prop_name,
              self.obj.props[self.prop_name] if self.prop_name in self.obj.props
              else getattr(self.obj, self.prop_name, None), self.other_value))

class SchemaConflict (ObjectError):

  def __init__ (self, obj, other):
    super().__init__(obj)
    self.other = other

  def __str__ (self):
    return "{}, is present in schema as {}".format(
      super().__str__(), _with_location(self.other))

class TypeConflict (ObjectError):

  def __init__ (self, obj, wrongtype='a different type'):
    super().__init__(obj)
    self.wrongtype = wrongtype

  def __str__ (self):
    return super().__str__() + ", exists as {}".format(self.wrongtype)

class DataTypeConflict (TypeConflict):

  def __init__ (self, obj, diff_props):
    super().__init__(obj)
    self.diff_props = diff_props

  def __str__ (self):
    return (super().__str__() + ": " +
        ", ".join("{} = {} but found {}"
                    .format(prop, self.obj.props[prop], found)
                  for prop, found in self.diff_props.items()))

class TableConflict (ObjectError):

  def __init__ (self, obj, tablename):
    super().__init__(obj)
    self.tablename = tablename

  def __str__ (self):
    return "{}, does not belong to expected table [{}]".format(
        super().__str__(), self.tablename)

class DataConflict (ObjectError):
  def __init__ (self, obj, msg):
    super().__init__(obj)
    self.msg = msg

  def __str__ (self):
    return "{}, {}".format(super().__str__(), self.msg)

class DuplicateIndexConflict (SchemaConflict):

  def __str__ (self):
    return "{} on columns {} duplicates {} on columns {}".format(
      self.obj.pretty_name, ", ".join(col.pretty_name
                                      for col in self.obj.columns),
      self.other.pretty_name, ", ".join(col.pretty_name
                                        for col in self.other.columns))

class NonexistentSchemaObjectError (ObjectError):
  def __init__ (self, obj):
    super().__init__(obj)

  def __str__ (self):
    return "{} does not exist".format(self.obj.pretty_name)

class MergeConflict (PrecogError):
  def __init__ (self, into_schema, source_schema):
    self.into_schema = into_schema
    self.source_schema = source_schema
    super().__init__(
      "While merging schema {} into {}".format(source_schema.name,
                                               into_schema.name))

  def __str__ (self):
    ret = super().__str__()
    if self.__context__:
      ret = "{}: {}".format(ret, self.__context__)
    return ret


class OracleNameError (PrecogError):
  pass

class ReservedNameError (OracleNameError):
  pass

class UndefinedVariableError (PrecogError):
  def __init__ (self, var_name):
    self.var_name = var_name

  def __str__ (self):
    return "{}{}".format(super().__str__(), self.var_name)

class UnsatisfiedDependencyError (PrecogError):

  def __init__ (self, unsatisfied):
    self.unsatisfied = unsatisfied

  def __str__ (self):
    return super().__str__() + "\n  ".join(line for obj in self.unsatisfied
                                           for line in (
      ['', "{} referenced by:".format(obj.pretty_name)] +
      ["  {}".format(_with_location(ref.from_))
       for ref in obj._referenced_by]))
