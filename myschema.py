from precog import *


schema = Schema('precog')

schema.add(Table('foo',
      [ Column('id', data_type='number')
      , Column('newcol', data_type='number', data_precision=3)
      , Column('colly', data_type='number', data_precision=3, data_scale=7)
      , Column('colbot', data_type='number', data_scale=2)
      , Column('text', data_type='varchar2', data_length=256) ])
      )

schema.add(Table('bar',
      [ Column('id', data_type='number')
      , Column('foo_id', data_type='number')
      , Column('body', data_type='varchar2', data_length=32) ])
      )

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
