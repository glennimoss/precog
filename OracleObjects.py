import cx_Oracle

class InsensitiveDict(dict):

  def __setitem__ (self, key, value):
    if isinstance(key, str):
      key = key.upper()

    super().__setitem__(key, value)

  def __getitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    return super().__getitem__(key)

  def __delitem__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    super().__delitem__(key)

  def __contains__ (self, key):
    if isinstance(key, str):
      key = key.upper()

    return super().__contains__(key)

class DBManager:

  def __init__ (self):
    self.connection = cx_Oracle.connect('gim', 'abc123', 'tkboi')
    self.curs = self.connection.cursor()

  def query (self, *args, **kvargs):
    self.curs.execute(*args, **kvargs)
    return [InsensitiveDict(
              zip((column[0] for column in self.curs.description), row)
            ) for row in self.curs]

  def execute (self, *args, **kvargs):
    self.curs.execute(*args, **kvargs)

    return self.curs.rowcount

db = DBManager()

class TypeConflict(Exception):

  def __init__ (self, obj, wrongtype):
    self.obj = obj
    self.wrongtype = wrongtype

  def __str__ (self):
    return "TypeConflict: {} [{}] exists as {}".format(
        self.obj.type(), self.obj.name, self.wrongtype) 

class OracleObject(object):

  def __init__ (self, name):
    self.name = name

  def type(self):
    return type(self).__name__.upper()

  def __str__ (self):
    return self.sql()

  def exists (self):
    rs = db.query(
        """ SELECT object_name, object_type
            FROM user_objects 
            WHERE object_name = :name
        """, name=self.name.upper())

    if not len(rs):
      return False

    rs = rs[0]
    if rs['object_type'] != self.type():
      raise TypeConflict(self, rs['object_type'])

    return True

  def create (self):
    if not self.exists():
      return db.execute(self.sql())

  def drop (self):
    if self.exists():
      return db.execute("DROP {} {}".format(self.type(), self.name))

  """ This is probably too powerful
  def force (self):
    try:
      return self.create()
    except TypeConflict as e:
      db.execute("DROP {} {}".format(e.wrongtype, self.name))
      return self.create()
  """





class Table(OracleObject):

  def __init__ (self, name, columns):
    super().__init__(name)
    self.columns = []
    for c in columns:
      self.columns.append(Column(*c, table=self))

  def sql (self):
    return "CREATE TABLE {} (\n    {}\n  )".format(self.name, 
        ',\n    '.join(c.sql() for c in self.columns))

class Column(OracleObject):

  def __init__ (self, name, datatype, table):
    super().__init__(name)
    self.datatype = datatype
    self.table = table

  def sql (self):
    return self.name + ' ' + self.datatype

if __name__ == '__main__':
  db = DBManager()

  rs = db.query('select * from foop')

  print(rs[0]['VALUE'])
