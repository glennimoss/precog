import logging

from precog.identifier import OracleIdentifier, name_from_oracle
from precog.util import InsensitiveDict
from precog.errors import OracleError

try:
  import cx_Oracle
except ImportError as e:
  logging.getLogger('precog.db').warn(
      "Unable to load cx_Oracle: {}\nUsing stub...".format(e))

  class DummyModule (object):
    class DummyConnection (object):
      class DummyCursor (list):
        def execute (self, *args, **kvargs):
          return []

        rowcount = 0

        description = []

        def close (self):
          pass

      def cursor (self):
        return self.DummyCursor()

      def close (self):
        pass

      username = 'dummy'

    def connect (self, connect_string):
      return self.DummyConnection()

    def close (self):
      pass

  cx_Oracle = DummyModule()

_connection = None
_numbers_as_strings = False
user = None
location = None

def connect (connect_string):
  global _connection, user
  if _connection:
    _connection.close()

  _connection = cx_Oracle.connect(connect_string)
  user = OracleIdentifier(_connection.username)
  location = "{}@{}".format(user, _connection.dsn)
  # The recyclebin causes problems when trying to drop several objects that
  # depend on each other.
  execute('ALTER SESSION SET RECYCLEBIN=OFF')
  # TODO: pass this in as a command-line parameter
  #execute("ALTER SESSION SET PLSQL_WARNINGS='ENABLE:ALL'")

def _rowfactory (row, cursor, oracle_names=[]):
  row = InsensitiveDict(zip((column[0] for column in cursor.description), row))
  for column in cursor.description:
    if column[1] == cx_Oracle.CURSOR:
      subcursor = row[column[0]]
      row[column[0]] = [_rowfactory(subrow, subcursor, oracle_names)
          for subrow in subcursor]
      subcursor.close()
  for column_name in oracle_names:
    if column_name in row:
      row[column_name] = name_from_oracle(row[column_name])
  return row

def _unquote (d):
  for k in d:
    if isinstance(d[k], OracleIdentifier):
      d[k] = d[k].strip('"')

def query (*args, oracle_names=[], **kvargs):
  cursor = _execute(*args, **kvargs)
  rs = [_rowfactory(row, cursor, oracle_names) for row in cursor]
  cursor.close()
  return rs

def execute (*args, **kvargs):
  cursor = _execute(*args, **kvargs)
  rc = cursor.rowcount
  cursor.close()
  return rc

def _execute(*args, **kvargs):
  if not _connection:
    raise OracleError('Not connected')

  _unquote(kvargs)
  cursor = _connection.cursor()
  cursor.numbersAsStrings = _numbers_as_strings
  try:
    cursor.execute(*args, **kvargs)
  except cx_Oracle.DatabaseError as e:
    offset = e.args[0].offset
    lines = args[0].split('\n')
    pos = 0
    for lineno in range(len(lines)):
      linelen = len(lines[lineno]) + 1
      if pos + linelen > offset:
        break
      pos += linelen
    offset -= pos

    lines.insert(lineno + 1, "{}^".format(' '*offset))
    sql = "\n".join(lines)

    raise OracleError("{}SQL:\n{}".format(e, sql)) from e
  return cursor

class all_strings (object):
  def __enter__ (self):
    global _numbers_as_strings
    self.orig_str_setting = _numbers_as_strings
    _numbers_as_strings = True
    return self

  def __exit__ (self, *args):
    global _numbers_as_strings
    _numbers_as_strings = self.orig_str_setting
