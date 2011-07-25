from precog import *

foo = Table('foo',
      [ ('id', 'number')
      , ('newcol', 'number', None, 3)
      , ('text', 'varchar2', 100) ])

bar = Table('bar',
      [ ('id', 'number')
      , ('foo_id', 'number')
      , ('body', 'varchar2', 32) ])

schema = [foo, bar]

diffs = []

for t in schema:
  try:
    print(t.name + ': ', end='')
    diff = t.diff()
    if diff:
      print('Differences found')
      diffs.extend(diff)
    else:
      print('Valid')

    print()
  except TypeConflict as e:
    print(e)

if diffs:
  print('Delta script:')
  print(";\n\n".join(diffs) + ";\n")

  doit = input('Run script? [yN] ')

  if 'y' == doit.lower():
    for diff in diffs:
      db.execute(diff)

