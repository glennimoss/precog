from precog import *


schema = Schema('precog')

schema.add(Table('foo',
      [ ('id', 'number')
      , ('newcol', 'number', None, 3)
      , ('colly', 'number', None, 3, 7)
      , ('colbot', 'number', None, None, 2)
      , ('text', 'varchar2', 100) ])
      )

schema.add(Table('bar',
      [ ('id', 'number')
      , ('foo_id', 'number')
      , ('body', 'varchar2', 32) ])
      )

diffs = []

for t in schema.objects[Table].values():
  try:
    print(str(t.name) + ': ', end='')
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

