#!/usr/bin/python3

import sys
import logging

from precog.objects import Database
from precog.errors import OracleError

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

connect_string = sys.argv[1]
schema_name = connect_string.split('/')[0]
database = Database.from_file(sys.argv[2], schema_name)

diffs = database.diff_to_db(connect_string)

if diffs:
  print('Delta script:')
  print(";\n\n".join(str(diff) for diff in diffs) + ";\n")

  doit = input('Run script? [yN] ')

  if 'y' == doit.lower():
    for diff in diffs:
      try:
        diff.apply()
      except OracleError as e:
        print(e)
