import argparse, logging, os, re, sys

from precog.objects.database import Database
from precog.errors import PrecogError, OracleError, UnappliedDependencyError
from precog.util import progress_print, pluralize

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
parser.add_argument('file', nargs='?', type=argparse.FileType('r'),
    help='SQL*Plus script to parse')

# Output control options
output_group = parser.add_mutually_exclusive_group()
output_group.add_argument('-v', '--verbose', action='append_const', const=True,
    help='Verbose logging. Specify twice for more output.')
output_group.add_argument('-q', '--quiet', action='store_true',
    help='Suppress output')

# Configuration options
parser.add_argument('--schema',
    help='Schema name for unqualified object names. Defaults to <username>.')
parser.add_argument('--dump', action='store_true',
    help='Dump specified schema.')
parser.add_argument('-t', '--table', action='append',
                    help='Specify a table name to dump its data. Repeat as '
                    'needed. Columns can be specified like TABLE:COL1,COL2,...')

# User-input options
prompt_group = parser.add_mutually_exclusive_group()
prompt_group.add_argument('-y', '--apply', action='store_true',
  help='Apply all changes without asking.')
prompt_group.add_argument('-n', '--no-apply', action='store_true',
  help='Do not ask or apply any changes.')

# Now GO!
args = parser.parse_args()

if not args.file and not args.dump:
  parser.error('Provide a file, or --dump')

# Configure logger
log_config = {'style': '{', 'format': '{levelname}: {message}'}
if args.quiet:
  sys.stdout = open(os.devnull, 'w')
  log_config['stream'] = sys.stdout
elif args.verbose:
  if len(args.verbose) > 1:
    log_config['format'] = '{levelname} {name}: {message}'
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

  if args.file:
    database = Database.from_file(args.file, schema_name)

    diffs = database.diff_to_db(args.connect_string)

    if diffs:
      retry = '.'
      while True:
        changes = sum(1 for diff in diffs if diff.priority)
        change_str = pluralize(changes, 'change')
        print("Found {}{}\n".format(change_str, retry),
              file=sys.stderr)
        print("\n\n".join(diff.formatted(args.no_apply, True)
                          for diff in diffs))
        print()

        if args.no_apply:
          break

        if not args.apply:
          doit = input("Apply {}? [yN] ".format(change_str))
        else:
          doit = 'y'

        errors = 0
        errored_objs = set()
        unapplied_diffs = []
        if 'y' == doit.lower():
          print("Applying {}...".format(change_str), file=sys.stderr)
          for diff in progress_print(diffs, "Applied {} of changes."):
            try:
              if diff.dependencies & errored_objs:
                raise UnappliedDependencyError(
                  "Unable to apply change due to an error in a dependency\n"
                  "SQL: {}".format(diff.sql))
              diff.apply()
            except PrecogError as e:
              print(e, file=sys.stderr)
              errored_objs.add(diff)
              unapplied_diffs.append(diff)
              if diff.produces:
                errored_objs.update(diff.produces)
              if diff.priority:
                errors += 1
          if errors:
            print("\nUnable to apply {}.".format(pluralize(errors, 'change')),
                  file=sys.stderr)
          successes = changes - errors
          print("Successfully applied {}."
                .format(pluralize(successes, 'change')), file=sys.stderr)
        if not errors:
          # We're done here
          break
        if not successes:
          # Terminate with a nonzero status code
          sys.exit(1)
        # Let's retry those that didn't work
        diffs = unapplied_diffs
        retry = ' that can be retried.'

    else:
      print('Database "{}@{}" is up to date with {}'.format(args.username,
                                                            args.dsn,
                                                            args.file.name),
          file=sys.stderr)

  elif args.dump:
    diffs = Database.dump_schema(args.connect_string, schema_name, args.table)
    print("\n\n".join(str(diff) for diff in diffs))

except PrecogError as e:
  print(e, file=sys.stderr)
  if args.verbose and len(args.verbose) > 1:
    raise
