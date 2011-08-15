class PrecogError (Exception):

  def __str__ (self):
    return "{}: {}".format(type(self).__name__, super().__str__())

class OracleError (PrecogError):
  pass

class ObjectError (PrecogError):

  def __init__ (self, obj):
    self.obj = obj

  def __str__ (self):
    return "{} [{}]".format(self.obj.type, self.obj.name)

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
        [''] + ["{} {} referenced by {}".format(type(obj).__name__, obj.name,
          ", ".join(" ".join((type(ref).__name__, str(ref.name)))
          for ref in obj.referenced_by()))
        for obj in self.unsatisfied])
