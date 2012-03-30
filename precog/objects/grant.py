from precog import db
from precog.diff import Diff, Reference
from precog.identifier import *
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp

_HasOnObj = HasProp('on_obj', assert_type=OracleObject,
                    dependency=Reference.AUTODROP)
_HasPrivileges = HasProp('privileges', assert_collection=set, assert_type=str)
class Grant (_HasOnObj, _HasPrivileges, OracleObject):

  def __init__ (self, grantee, **props):
    super().__init__(OracleFQN(grantee, '__GRANT_PLACEHOLDER'), **props)

  @_HasPrivileges.privileges.setter
  def privileges (self, value):
    _HasPrivileges.privileges.__set__(self, value)
    self._privileges = {p.upper() for p in self.privileges}

  @_HasOnObj.on_obj.setter
  def on_obj (self, value):
    _HasOnObj.on_obj.__set__(self, value)
    self.name = self.name.with_(obj=value.name.schema, part=value.name.obj)

  def _sql (self, fq=True):
    on_obj = self.on_obj.name
    if not fq:
      on_obj = on_obj.obj

    return "GRANT {} ON {} TO {}".format(', '.join(self.privileges),
                                         on_obj.lower(),
                                         self.name.schema.lower())

  def _drop (self):
    return Diff("REVOKE {} ON {} FROM {}".format(', '.join(self.privileges),
                                                 self.on_obj.name.lower(),
                                                 self.name.schema.lower()),
                self, priority=Diff.DROP)

  @classmethod
  def from_db (class_, schema, into_database, _):
    rs = db.query(""" SELECT privilege
                           , owner
                           , table_name
                      FROM dba_tab_privs
                      WHERE grantee = :o
                      ORDER BY owner, table_name
                      """, o=schema, oracle_names=['owner', 'table_name'])

    def group (iter):
      grant = None
      try:
        row = next(iter)
        obj_name = OracleFQN(row['owner'], row['table_name'])
        while True:
          grant = {'privs': set(),
                   'name': obj_name}
          while obj_name == grant['name']:
            grant['privs'].add(row['privilege'])
            row = next(iter)
            obj_name = OracleFQN(row['owner'], row['table_name'])

          yield grant
      except StopIteration:
        if grant:
          yield grant


    for grant in group(rs):
      yield class_(grant['name'].schema, privileges=set(grant['privs']),
                   on_obj=into_database.find(grant['name'], OracleObject),
                   database=into_database, create_location=(db.location,))
    rs.close()
