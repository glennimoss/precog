from precog.util import InsensitiveDict
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


def query (*args, **kvargs):
  _curs.execute(*args, **kvargs)
  return [InsensitiveDict(
            zip((column[0] for column in _curs.description), row)
          ) for row in _curs]

def execute (*args, **kvargs):
  _curs.execute(*args, **kvargs)

  return _curs.rowcount
