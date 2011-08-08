def foo (arg):
  def _foo (self):
    print(arg)
  return _foo

class A (object):
  def __init__ (self):
    self.foo = foo('A')

class B (object):
  def __init__ (self):
    self.foo = foo('B')

a = A()
b = B()
a.foo()
b.foo()
