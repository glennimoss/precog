#!/usr/bin/python3

import sys
import logging

from precog.objects import Database

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.getLogger('precog.objects.Column').setLevel(logging.DEBUG)
logging.getLogger('precog.objects.Schema').setLevel(logging.DEBUG)

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
      diff.apply()
