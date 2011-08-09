#!/usr/bin/python3

import sys
import logging

from precog.objects import Database

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

database = Database.from_file(sys.argv[2])

diffs = database.diff_to_db(sys.argv[1])

if diffs:
  print('Delta script:')
  print(";\n\n".join(str(diff) for diff in diffs) + ";\n")

  doit = input('Run script? [yN] ')

  if 'y' == doit.lower():
    for diff in diffs:
      db.execute(str(diff))
