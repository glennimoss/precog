class Foo(object):
  bar = 'baz'

  def __init__ (self, arg = None):
    if arg:
      Foo.bar = arg

  def getBar (this):
    return this.bar

a = Foo()
repr(super(a))
