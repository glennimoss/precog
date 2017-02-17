from precog import db
from precog.identifier import OracleFQN, schema_alias
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp

_HasForName = HasProp('for_name', assert_type=OracleFQN)
class Synonym (_HasForName, OracleObject):

  @_HasForName.for_name.getter
  def for_name (self):
    name = _HasForName.for_name.__get__(self)
    if name:
      if name.schema is None:
        name = name.with_(schema=self.database.default_schema)
      else:
        name = name.with_(schema=schema_alias(name.schema))
    return name

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
    into_database.log.debug("Querying for synonyms {} from DB...".format(
      "(all)" if synonym_names is None else ", ".join(synonym_names)))
    rs = db.query(""" SELECT synonym_name
                           , table_owner
                           , table_name
                      FROM dba_synonyms
                      WHERE owner = :o
                         {}
                  """.format(synonym_filter), o=schema,
                  oracle_names=['synonym_name', 'table_owner', 'table_name'])
    into_database.log.debug("Cursor obtained")
    for row in rs:
      into_database.log.debug("Processing synonym {}".format(row['synonym']))
      yield class_(OracleFQN(schema, row['synonym_name']),
                   for_name=OracleFQN(row['table_owner'], row['table_name']),
                   database=into_database, create_location=(db.location,))
    rs.close()
