from precog.util import InsensitiveDict
import cx_Oracle

_connection = cx_Oracle.connect('gim', 'abc123', 'tkboi')
_curs = _connection.cursor()

def query (*args, **kvargs):
  _curs.execute(*args, **kvargs)
  return [InsensitiveDict(
            zip((column[0] for column in _curs.description), row)
          ) for row in _curs]

def execute (*args, **kvargs):
  _curs.execute(*args, **kvargs)

  return _curs.rowcount
