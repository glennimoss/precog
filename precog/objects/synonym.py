from precog.objects.base import OracleObject

class Synonym (OracleObject):

  def __init__ (self, name, for_object=None, **props):
    super().__init__(name, **props)
    self.for_object = for_object

  @property
  def for_object (self):
    return self._for_object

  @for_object.setter
  def for_object (self, obj):
    _assert_type(obj, OracleObject)
    self._depends_on(obj, '_for_object', Reference.SOFT)
    self.props['for_object'] = obj.name

  def _sql (self, fq=True):
    name = self.name.obj
    if fq:
      name = self.name

    return "CREATE OR REPLACE SYNONYM {} FOR {}".format(name.lower(),
        self.for_object.name.lower())

  def recreate (self, other):
    return self.create()

  @classmethod
  def from_db (class_, name, into_database):
    rs = db.query(""" SELECT table_owner
                           , table_name
                      FROM dba_synonyms
                      WHERE owner = :o
                        AND synonym_name = :n
                  """, o=name.schema, n=name.obj)
    if not rs:
      return None
    rs = rs[0]
    return class_(name, into_database.find(OracleFQN(rs['table_owner'],
                                                     rs['table_name']),
                                           OracleObject),
                  database=into_database)
