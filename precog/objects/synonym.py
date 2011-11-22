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
                   for_object=into_database.find(OracleFQN(row['table_owner'],
                                                           row['table_name']),
                                                 OracleObject),
                   database=into_database, create_location=(db.location,))
    rs.close()
