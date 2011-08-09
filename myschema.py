from precog import *


database = Database.from_file('test.sql')

def diffs():
  diffs = database.diff_to_db()

  if diffs:
    print('Delta script:')
    print(";\n\n".join(str(diff) for diff in diffs) + ";\n")

    doit = input('Run script? [yN] ')

    if 'y' == doit.lower():
      for diff in diffs:
        db.execute(str(diff))

  return diffs

d = diffs()
