def test_property_mixin ():
  class A (object):
    @property
    def foo (self):
      print('A.foo getter')
      return self._foo

    @foo.setter
    def foo (self, foo):
      print('A.foo setter')
      self._foo = 'A' + foo

  class B (A):

    @A.foo.setter
    def foo (self, foo):
      print('B.foo setter')
      A.foo.__set__(self, 'B' + foo)

  a = A()
  a.foo = 'cool'
  print("a.foo = {}".format(a.foo))

  b = B()
  b.foo = 'beans'
  print("b.foo = {}".format(b.foo))

def test_mixin_mro ():
  class A (object):
    def foo (self):
      print('A.foo')

  class Mixin (object):
    def foo (self):
      print('Mixin.foo')
      super().foo()

  class B (Mixin, A):
    def foo (self):
      print('B.foo')
      super().foo()

  b = B()
  b.foo()

test_mixin_mro()
