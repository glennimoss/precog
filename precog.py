#!/usr/bin/python3

import argparse, logging, os, sys

from precog.objects import Database
from precog.errors import OracleError

# TODO: silly os doesn't pass in COLUMNS envvar... so 80 is assumed :(
class HelpyArgparser(argparse.ArgumentParser):
  def error (self, message):
    if len(sys.argv) != 1:
      sys.stderr.write("error: {}\n".format(message))
    self.print_help()
    sys.exit(1)

parser = HelpyArgparser(description='Generate Oracle migration script.',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('connect_string',
    metavar='<username>/<password>@<connect_identifier>', type=str,
    help='Oracle connection string')
parser.add_argument('file', type=argparse.FileType('r'),
    help='SQL*Plus script to parse')
parser.add_argument('-v', '--verbose', action='append_const', const=True,
    help='Verbose logging. Specify twice for more output.')
parser.add_argument('-q', '--quiet', action='store_true',
    help='Suppress output')
args = parser.parse_args()

log_config = {'style': '{', 'format': '{levelname}: {message}'}
if args.quiet:
  sys.stdout = open(os.devnull, 'w')
  log_config['stream'] = sys.stdout
elif args.verbose:
  if len(args.verbose) > 1:
    log_config['level'] = logging.DEBUG
  else:
    log_config['level'] = logging.INFO
else:
  log_config['level'] = logging.WARN
  logging.basicConfig(level=logging.WARN)
logging.basicConfig(**log_config)

try:
  schema_name = args.connect_string.split('/')[0]
  database = Database.from_file(args.file, schema_name)

  diffs = database.diff_to_db(args.connect_string)

  if diffs:
    print("Found {} changes:".format(len(diffs)))
    print(";\n\n".join(str(diff) for diff in diffs) + ";\n")

    doit = input('Run script? [yN] ')

    errors = 0
    if 'y' == doit.lower():
      for diff in diffs:
        try:
          diff.apply()
        except OracleError as e:
          print(e)
          errors += 1
    if errors:
      print()
      print("Unable to apply {} changes.".format(errors))

  else:
    print("Oracle is up to date with {}".format(args.file.name))
except Exception as e:
  print(e)
