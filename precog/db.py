from precog.identifier import OracleIdentifier
from precog.util import InsensitiveDict
from precog.errors import OracleError

try:
  import cx_Oracle

  _connection = cx_Oracle.connect('precog', 'abc123', 'xe')
  _curs = _connection.cursor()
except ImportError as e:
  print('Unable to load cx_Oracle:', e, '\nUsing stub...')
  class DummyCursor (list):
    def execute (self, *args, **kvargs):
      return []

    rowcount = 0

    description = []

  _curs = DummyCursor()

def _rowfactory (row, cursor=_curs):
  row = InsensitiveDict(zip((column[0] for column in cursor.description), row))
  for column in cursor.description:
    if column[1] == cx_Oracle.CURSOR:
      subcursor = row[column[0]]
      row[column[0]] = [_rowfactory(subrow, subcursor) for subrow in subcursor]
  return row

def _unquote (d):
  for k in d:
    if isinstance(d[k], OracleIdentifier):
      d[k] = d[k].strip('"')

def query (*args, **kvargs):
  execute(*args, **kvargs)
  return [_rowfactory(row) for row in _curs]

def execute (*args, **kvargs):
  _unquote(kvargs)
  try:
    _curs.execute(*args, **kvargs)
  except cx_Oracle.DatabaseError as e:
    raise OracleError("{}SQL: {}".format(e, args[0])) from e

  return _curs.rowcount

user = OracleIdentifier(_connection.username)
