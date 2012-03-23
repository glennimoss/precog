from precog import db
from precog.diff import Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp

_HasOnObj = HasProp('on_obj', assert_type=OracleObject,
                    dependency=Reference.AUTODROP)
_HasPrivileges = HasProp('privileges', assert_collection=list, assert_type=str)
_HasGrantee = HasProp('grantee', assert_type=OracleIdentifier)
class Grant (_HasOnObj, _HasPrivileges, _HasGrantee, OracleObject):

  def __init__ (self, **props):
    super().__init__('placeholder', **props)

  @property
  def name (self):
    return self._name

  @name.setter
  def name (self, value):
    self._name = value
    if value.schema is not None:
      self.grantee = value.schema

  @_HasGrantee.grantee.setter
  def grantee (self, value):
    _HasGrantee.grantee.__set__(self, value)
    if self.name.schema is None:
      self.name = self.name.with_(schema=value)

  @_HasPrivileges.privileges.setter
  def privileges (self, value):
    _HasPrivileges.privileges.__set__(self, value)
    self._privileges = [p.upper() for p in self.privileges]
    self.name = self.name.with_(
      obj=OracleIdentifier("{}".format(','.join(self.privileges)), True))

  @_HasOnObj.on_obj.setter
  def on_obj (self, value):
    _HasOnObj.on_obj.__set__(self, value)
    self.name = self.name.with_(part=OracleIdentifier("{}".format(value), True))

  def _sql (self, fq=True):
    grantee = self.grantee
    on_obj = self.on_obj
    if not fq:
      grantee = grantee.obj
      on_obj = on_obj.obj

    return "GRANT {} ON {} TO {}".format(', '.join(self.privileges),
                                         on_obj.lower(), grantee.lower())

  def recreate (self, other):
    return [self.create()]

  @classmethod
  def from_db (class_, schema, into_database, synonym_names=None):
    synonym_filter = db.filter_clause('synonym_name', synonym_names)
    rs = db.query(""" SELECT grantee
                           , privilege
                           , owner
                           , table_name
                      FROM dba_tab_privs
                      WHERE grantee = :o
                         {}
                  """.format(synonym_filter), o=schema,
                  oracle_names=['grantee', 'owner', 'table_name'])
    for row in rs:
      yield class_(grantee=row['grantee'], privilege=row['privilege'],
                   on_obj=into_database.find(OracleFQN(row['owner'],
                                                       row['table_name']),
                                             OracleObject),
                   database=into_database, create_location=(db.location,))
    rs.close()
