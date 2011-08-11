import argparse, logging, os, re, sys

from precog.objects import Database
from precog.errors import PrecogError, OracleError

#Always print help
class HelpyArgparser(argparse.ArgumentParser):
  def error (self, message):
    if len(sys.argv) != 1:
      sys.stderr.write("error: {}\n".format(message))
    self.print_help()
    sys.exit(1)

# Validate connection string
class ConnectionStringAction (argparse.Action):
  metavar = '<username>/<password>@<dsn>'
  def __call__ (self, parser, namespace, values, option_string=None):
    match = re.match(r'^("[^"]+"|[\w$#]+)/("[^"]+"|[^/@]+)@(.+)$', values)
    if not match:
      parser.error("Connection string does not match {}".format(self.metavar))

    setattr(namespace, self.dest, values)
    namespace.username, namespace.password, namespace.dsn = match.groups()


parser = HelpyArgparser(description='Generate Oracle migration script.')


# Positional arguments
parser.add_argument('connect_string',
    metavar=ConnectionStringAction.metavar, action=ConnectionStringAction,
    help='Oracle connection string')
parser.add_argument('file', type=argparse.FileType('r'),
    help='SQL*Plus script to parse'
    )

# Output control options
output_group = parser.add_mutually_exclusive_group()
output_group.add_argument('-v', '--verbose', action='append_const', const=True,
    help='Verbose logging. Specify twice for more output.')
output_group.add_argument('-q', '--quiet', action='store_true',
    help='Suppress output')

# Configuration options
parser.add_argument('--schema',
    help='Schema name for unqualified object names. Defaults to <username>.')

# User-input options
prompt_group = parser.add_mutually_exclusive_group()
prompt_group.add_argument('-y', '--apply', action='store_true',
  help='Apply all changes without asking.')
prompt_group.add_argument('-n', '--no-apply', action='store_true',
  help='Do not ask or apply any changes.')

# Now GO!
args = parser.parse_args()

# Configure logger
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
logging.basicConfig(**log_config)

# Precog time
try:
  schema_name = args.username
  if args.schema:
    schema_name = args.schema
  database = Database.from_file(args.file, schema_name)

  diffs = database.diff_to_db(args.connect_string)

  if diffs:
    print("Found {} changes:".format(len(diffs)))
    print(";\n\n".join(str(diff) for diff in diffs) + ";\n")

    if not (args.apply or args.no_apply):
      doit = input('Run script? [yN] ')
    else:
      doit = 'y' if args.apply else 'n'

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
except PrecogError as e:
  print(e)
