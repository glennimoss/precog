from precog import *
from precog.parser import sqlLexer, sqlParser


schema = Schema.fromFile('precog', 'test.sql')

def diffs():
  dbschema = Schema.fromDb('precog')
  #dbschema = Schema('precog')
  #dbschema.add(Table.fromDb(OracleFQN('precog','foo')))
  #dbschema.add(Table.fromDb(OracleFQN('precog','bar')))

  diffs = schema.diff(dbschema)

  if diffs:
    print('Delta script:')
    print(";\n\n".join(diffs) + ";\n")

    doit = input('Run script? [yN] ')

    if 'y' == doit.lower():
      for diff in diffs:
        db.execute(diff)

  return diffs

d = diffs()
