from precog import db
from precog.diff import Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp

class Synonym (HasProp('for_object', dependency=Reference.SOFT,
                       assert_type=OracleObject),
               OracleObject):


  def _eq_for_object (self, other):
    return self.for_object.name == other.for_object.name

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
      into_database.log.warn("Synonym not found for {}".format(name))
      return None
    rs = rs[0]
    return class_(name, for_object=into_database.find(
      OracleFQN(rs['table_owner'], rs['table_name']), OracleObject),
      database=into_database, create_location=(db.location))
