import cx_Oracle
from precog.identifier import OracleIdentifier, name_from_oracle
from precog.util import InsensitiveDict
from precog.errors import OracleError

_connection = None
_curs = None
user = None

def connect (connect_string):
  global _connection, _curs, user
  if _curs:
    _curs.close()
  if _connection:
    _connection.close()
  try:
    _connection = cx_Oracle.connect(connect_string)
    user = OracleIdentifier(_connection.username)
    _curs = _connection.cursor()
  except ImportError as e:
    print('Unable to load cx_Oracle:', e, '\nUsing stub...')
    class DummyCursor (list):
      def execute (self, *args, **kvargs):
        return []

      rowcount = 0

      description = []

    _curs = DummyCursor()

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
  execute(*args, **kvargs)
  return [_rowfactory(row, _curs, oracle_names) for row in _curs]

def execute (*args, **kvargs):
  if not _curs:
    raise OracleError('Not connected')

  _unquote(kvargs)
  try:
    _curs.execute(*args, **kvargs)
  except cx_Oracle.DatabaseError as e:
    raise OracleError("{}SQL: {}".format(e, args[0])) from e

  return _curs.rowcount

