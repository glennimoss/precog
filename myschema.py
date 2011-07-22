from precog import *

foo = Table('foo',
      [ ('id', 'number')
      , ('text', 'varchar2', 100) ])

bar = Table('bar', 
      [ ('id', 'number') 
      , ('foo_id', 'number')
      , ('body', 'varchar2', 33) ])

schema = [foo, bar]

for t in schema:
  try:
    print(t)
    print('Created:', bool(t.create()))
    print()
  except TypeConflict as e:
    print(e)


