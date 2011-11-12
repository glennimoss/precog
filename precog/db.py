import logging, math

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
        def execute (self, *args, **kwargs):
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
_max_cursors = 300
user = None
location = None

def connect (connect_string):
  global _connection, _max_cursors, user, location
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
  _max_cursors = int(query(""" SELECT value
                               FROM v$parameter
                               WHERE name = 'open_cursors'
                           """)[0]['value'])

def _fetchall (cursor, args=[], kwargs={}, oracle_names=[]):
  cursor_desc = cursor.description
  cursor.arraysize = 1000
  cursors_in_query = sum(1 for c in cursor_desc if c[1] == cx_Oracle.CURSOR)
  if cursors_in_query:
    # WARNING: if subcursors have subcursors, there won't be enough left and
    # they'll error out. Not sure the best way to handle that case, so I won't.
    cursor.arraysize = math.floor((_max_cursors - 1)/cursors_in_query/2)

  column_names = [column[0] for column in cursor_desc]
  def rowfactory (*row):
    row = InsensitiveDict(zip(column_names, row))
    for column in cursor_desc:
      if column[1] == cx_Oracle.CURSOR:
        subcursor = row[column[0]]
        row[column[0]] = _fetchall(subcursor, oracle_names=oracle_names)

    for column_name in oracle_names:
      if column_name in row:
        row[column_name] = name_from_oracle(row[column_name])
    return row
  cursor.rowfactory = rowfactory

  if cursor.statement:
    cursor.execute(None, *args, **kwargs)
  return cursor.fetchall()

def _unquote (d):
  for k in d:
    if isinstance(d[k], OracleIdentifier):
      d[k] = d[k].strip('"')

def query (sql, *args, oracle_names=[], **kwargs):
  cursor = _execute(sql, *args, parse_only=True, **kwargs)
  rs = _fetchall(cursor, args, kwargs, oracle_names)
  cursor.close()
  return rs

def execute (*args, **kwargs):
  cursor = _execute(*args, **kwargs)
  rc = cursor.rowcount
  cursor.close()
  return rc

def _execute(sql, *args, parse_only=False, **kwargs):
  if not _connection:
    raise OracleError('Not connected')

  _unquote(kwargs)
  cursor = _connection.cursor()
  cursor.numbersAsStrings = _numbers_as_strings
  try:
    if parse_only:
      cursor.parse(sql.encode())
    else:
      cursor.execute(sql, *args, **kwargs)
  except cx_Oracle.DatabaseError as e:
    offset = e.args[0].offset
    lines = sql.split('\n')
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
