class PrecogError (Exception):

  def __str__ (self):
    return "{}: {} [{}]".format(type(self), self.obj.type, self.obj.name)

class TypeConflict (PrecogError):

  def __init__ (self, obj, wrongtype='a different type'):
    self.obj = obj
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

class OracleNameError (PrecogError):
  pass

