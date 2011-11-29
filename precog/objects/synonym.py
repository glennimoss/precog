from precog import db
from precog.diff import Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp

_HasForName = HasProp('for_name', assert_type=OracleFQN)
class Synonym (_HasForName, OracleObject):

  @_HasForName.for_name.setter
  def for_name (self, value):
    _HasForName.for_name.__set__(self, value)
    if self.for_name.schema is None:
      self._for_name = self.for_name.with_(schema=self.name.schema)

  @property
  def name (self):
    return self._name

  @name.setter
  def name (self, value):
    self._name = value
    if (self.for_name and self.for_name.schema is None and
        self._name.schema is not None):
      self.for_name = self.for_name

  def _sql (self, fq=True):
    name = self.name
    for_name = self.for_name
    if not fq:
      name = name.obj
      for_name = for_name.obj

    return "CREATE OR REPLACE SYNONYM {} FOR {}".format(name.lower(),
                                                        for_name.lower())

  def recreate (self, other):
    return [self.create()]

  @classmethod
  def from_db (class_, schema, into_database, synonym_names=None):
    synonym_filter = db.filter_clause('synonym_name', synonym_names)
    rs = db.query(""" SELECT synonym_name
                           , table_owner
                           , table_name
                      FROM dba_synonyms
                      WHERE owner = :o
                         {}
                  """.format(synonym_filter), o=schema,
                  oracle_names=['synonym_name', 'table_owner', 'table_name'])
    for row in rs:
      yield class_(OracleFQN(schema, row['synonym_name']),
                   for_name=OracleFQN(row['table_owner'], row['table_name']),
                   database=into_database, create_location=(db.location,))
    rs.close()
