from precog.objects import Table, Column

definition = Table('foo', [ Column('id', data_type='number') ])
current_state = Table('foo',
    [ Column('oldid', data_type='varchar2', data_length=16) ])

diffs = definition.columns[0].diff(current_state.columns[0])

print(diffs)
assert diffs == [ "ALTER TABLE FOO RENAME COLUMN OLDID TO ID"
                , "ALTER TABLE FOO MODIFY ( ID NUMBER )"
                ]

