class PrecogError (Exception):

  def __str__ (self):
    return "{}: {}".format(type(self).__name__, super().__str__())

class UnimplementedFeatureError (PrecogError):
  pass

class ParseError (PrecogError):

  def __init__ (self, num_errors):
    self.num_errors = num_errors

  def __str__ (self):
    return "{}{} error{} in schema definition".format(super().__str__(),
        self.num_errors, 's' if self.num_errors > 1 else '')

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
    return '{}{}\n  {}, line {}\n    {}\n    {}^{}'.format(
      super(ParseError, self).__str__(), self.title, self.source_name,
      self.line, self.line_text, ' '*(self.column),
      "\n{}".format(self.explanation) if self.explanation else '')

class SqlSyntaxError (SyntaxError):
  pass

class OracleError (PrecogError):
  pass

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
      parts.append(str(SyntaxError(
          "PL/SQL compile {}:".format(error_props['attribute'].lower()),
          plsql_obj.pretty_name, line, error_props['position'] - 1,
          plsql_obj.sql().split('\n')[line-1], error_props['text'])))
    super().__init__("\n".join(parts))

class ObjectError (PrecogError):

  def __init__ (self, obj):
    self.obj = obj

  def __str__ (self):
    return self.obj.pretty_name

class SchemaConflict (ObjectError):

  def __init__ (self, obj, other):
    super().__init__(obj)
    self.other = other

  def __str__ (self):
    return "{} is present in schema as {}".format(
        super().__str__(), self.other.sql(fq=True))

class TypeConflict (ObjectError):

  def __init__ (self, obj, wrongtype='a different type'):
    super().__init__(obj)
    self.wrongtype = wrongtype

  def __str__ (self):
    return super().__str__() + " exists as {}".format(self.wrongtype)

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
    return "{} does not belong to expected table [{}]".format(
        super().__str__(), self.tablename)

class DataConflict (ObjectError):
  def __init__ (self, obj, msg):
    super().__init__(obj)
    self.msg = msg

  def __str__ (self):
    return "{} {}".format(super().__str__(), self.msg)

class DuplicateIndexConflict (SchemaConflict):

  def __str__ (self):
    return "{} duplicates {}".format(self.obj.pretty_name,
                                     self.other.pretty_name)

class OracleNameError (PrecogError):
  pass

class ReservedNameError (PrecogError):
  pass

class UnsatisfiedDependencyError (PrecogError):

  def __init__ (self, unsatisfied):
    self.unsatisfied = unsatisfied

  def __str__ (self):
    return super().__str__() + "\n  ".join(line for obj in self.unsatisfied
                                           for line in (
      ['', "{} referenced by:".format(obj.pretty_name)] +
      ['  {}, in "{}", line {}'.format(ref.from_.pretty_name,
                                       ref.from_.props.get('create_location',
                                                           ('',))[0],
                                       ref.from_.props.get('create_location',
                                                           ('', 0))[1])
       for ref in obj._referenced_by]))
