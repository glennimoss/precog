from antlr3.ext import NL_CHANNEL

class PrecogError (Exception):

  def __str__ (self):
    return "{}: {}".format(type(self).__name__, super().__str__())

class ParseError (PrecogError):

  def __init__ (self, title, source_name, line, column, line_text,
      explanation=''):
    self.title = title
    self.source_name = source_name
    self.line = line
    self.column = column
    self.line_text = line_text
    self.explanation = explanation

  def __str__ (self):
    return '{}{}\n  {}, line {}\n    {}\n    {}^\n{}'.format(
      super().__str__(), self.title, self.source_name, self.line,
      self.line_text, ' '*(self.column), self.explanation)

class SqlParseError (ParseError):
  def __init__ (self, error):
    from precog.parser.sqlParser import NL, EOF
    self.error = error

    error.input.mark()
    error.input.seek(error.index)
    error.input.add(NL_CHANNEL)

    def find (dir, test):
      p = dir
      while True:
        this_token = error.input.LT(p)
        if test(this_token):
          break;
        p += dir
      return this_token

    start_token = find(-1, lambda t: t is None or t.type == NL)
    end_token = find(1, lambda t: t.type in (NL, EOF))
    error.input.drop(NL_CHANNEL)
    error.input.rewind()

    line_text = (error.input.toString(start_token, end_token)
      .lstrip(start_token.text).rstrip(end_token.text))

    super().__init__(type(error).__name__,
        'File "{}"'.format(error.getSourceName()), error.line,
        error.charPositionInLine, line_text)

class OracleError (PrecogError):
  pass

class PlsqlParseError (ParseError, OracleError):

  def __init__ (self, plsql_obj, error_props):
    self.error = error_props
    line = error_props['line']
    super().__init__(
        "PL/SQL compile {}:".format(error_props['attribute'].lower()),
        plsql_obj.pretty_name, line, error_props['position'],
        plsql_obj.sql().split('\n')[line-1], error_props['text'])

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
        super().__str__(), self.other.sql(True))

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

class OracleNameError (PrecogError):
  pass

class ReservedNameError (PrecogError):
  pass

class UnsatisfiedDependencyError (PrecogError):

  def __init__ (self, unsatisfied):
    self.unsatisfied = unsatisfied

  def __str__ (self):
    return super().__str__() + "\n  ".join(
        [''] + ["{} referenced by {}".format(obj.pretty_name,
          ", ".join(ref.pretty_name for ref in obj.referenced_by()))
        for obj in self.unsatisfied])
