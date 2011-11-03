import logging, time

from precog.diff import Diff, Reference
from precog.identifier import *
from precog.util import classproperty, HasLog, InsensitiveDict

SkippedObject = object()
UnsetProperty = object()

class OracleObject (HasLog):

  @classproperty
  def type (class_):
    if hasattr(class_, 'namespace'):
      class_ = class_.namespace
    return class_.pretty_type.upper()

  @classproperty
  def pretty_type (class_):
    return re.sub('([A-Z])', r' \1', class_.__name__).strip()

  def __init__ (self, name, deferred=False, database=None, reinit=False,
                create_location=None, **props):
    if not isinstance(name, OracleFQN):
      name = OracleFQN(obj=name)
    self.name = name

    if not reinit:
      super().__init__()
      self.create_location = create_location
      self.deferred = deferred
      self.database = database
      self.props = InsensitiveDict(props)
      self._referenced_by = set()
      self._dependencies = set()

      # Ugh this feels hacky
      self._ignore_name = False

  def __repr__ (self, **other_props):
    #return super().__repr__()
    return "<{}>".format(self.pretty_name)
    #if self.deferred:
      #other_props['deferred'] = True

    #props = self.props.copy()
    #props.update(other_props)
    #return "{}({!r}, {})".format(type(self).__name__,
        #self.name,
        #', '.join("{}={!r}".format(k, v) for k, v in props.items()))

  def __str__ (self):
    return self.sql()

  @property
  def create_location (self):
    if not self._create_location:
      return ['unknown']
    return self._create_location

  @create_location.setter
  def create_location (self, value):
    self._create_location = value
    if value:
      self._create_location = []
      self._create_location.append('in "{}"'.format(value[0]))
      if len(value) > 1:
        self._create_location.append('line {}'.format(value[1]))

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      #self.log.debug(
        #"instanceof({}, type({})) failed for type(other) = {!r}, type(self) = "
        #"{!r}".format(self and self.pretty_name, other and other.pretty_name,
                      #type(other), type(self)))
      return False

    if not self._ignore_name and self.name != other.name:
      #self.log.debug(
        #"{} == {} failed for self.name = {!r}, other.name = {!r}".format(
          #self.pretty_name, other.pretty_name, self.name, other.name))
      return False

    common_props = self.props.keys() & other.props.keys()
    for prop_name in common_props:
      if self.props[prop_name] != other.props[prop_name]:
        return False

    return True

  def __hash__ (self):
    return hash((type(self), self.name))

  @property
  def pretty_name (self):
    return " ".join((self.pretty_type, self.name) +
                    ( ('*',) if self.name.generated else ()) +
                    (
                      (str(id(self)),) if self.log.isEnabledFor(logging.DEBUG)
                      else ()
                    ))

  def sql (self, **args):
    if not self.deferred:
      return self._sql(**args)
    return OracleObject._sql(self, **{'fq': args[k] for k in args if k == 'fq'})

  def _sql (self, fq=True):
    return "-- Placeholder for {}{}".format(
        'deferred ' if self.deferred else '', self.pretty_name)

  @property
  def sql_produces (self):
    return {self}

  def create (self):
    return [Diff(self.sql(), produces=self.sql_produces, priority=Diff.CREATE)]

  def drop (self):
    self.log.debug("Dropping {}".format(self.pretty_name))
    drop = self._drop()
    ref_diffs = self.teardown(drop=True)
    drop.add_dependencies(ref_diffs)
    return [drop] + ref_diffs

  def teardown (self, drop=False):
    """
    Disable or drop all depdendent objects. This is necessary in certain
    circumstances when modifying an object.
    """

    self.log.debug("Tearing down {}".format(self.pretty_name))
    for ref in self._referenced_by:
      self.log.debug(ref)
    return [diff for ref in self._referenced_by
              if ref.integrity is not Reference.SOFT
            for diff in ref.from_.drop()]

  def _drop (self):
    return Diff("DROP {} {}".format(self.type, self.name.lower()), self,
                priority=Diff.DROP)

  def recreate (self, other):
    """
    Recreate this object from scratch. Usually means a drop and a create.
    """
    drop, *diffs = other.drop()
    diffs.extend(diff
        for ref in self._referenced_by
          if ref.integrity in (Reference.AUTODROP, Reference.HARD)
        for diff in ref.from_.create())
    creates = self.create()
    for diff in creates:
      diff.add_dependencies(drop)
    diffs.append(drop)
    diffs.extend(creates)
    return diffs

  def rebuild (self):
    """
    Try to rebuild this object non-destructively. Used when the object is in an
    invalid state. If it can't be done non-destructively, it will attempt to
    recreate the object.
    """

    return self.recreate(self)

  def rename (self, other):
    return Diff("ALTER {} {} RENAME TO {}".format(self.type, other.name.lower(),
                                                  self.name.obj.lower()),
                produces=self)

  def satisfy (self, other):
    if self.deferred:
      if type(self) is not type(other):
        self.become(type(other))
      if self.name.generated and not other.name.generated:
        self.name = other.name
      elif other.name.generated:
        self.name._generated = True

      if not self._create_location:
        self._create_location = other.create_location

      for k, v in other.props.items():
        if k in self.props and self.props[k] is UnsetProperty:
          del self.props[k]
          # TODO: ACK! this is craziness
          del other.props[k]
        else:
          self.props[k] = v

      self.deferred = False

  def diff (self, other, recreate=True):
    """
    Calculate differences between self, which is the desired definition, and
    other, which is the current database state.
    """

    if other.deferred:
      self.log.warn(
          "Comparing {!r} to deferred object {!r}".format(self, other))
    if self != other:
      if recreate:
        return self.recreate(other)
      elif self.name.obj != other.name.obj:
        return [self.rename(other)]
    else:
      if other.props['status'] and other.props['status'] != 'VALID':
        self.log.debug("{} has status {}".format(other.pretty_name,
          other.props['status']))
        return other.rebuild()

    return []

  def _diff_props (self, other):
    prop_diff = InsensitiveDict((prop, expected)
                                for prop, expected in self.props.items()
                                if expected != other.props[prop])

    if self.log.isEnabledFor(logging.DEBUG):
      for prop in prop_diff:
        self.log.debug("{} ['{}']: expected {!r}, found {!r}".format(
          self.pretty_name, prop, self.props[prop], other.props[prop]))

    return prop_diff

  def diff_subobjects (self, other, get_objects, label=lambda x: x.name,
                       rename=True):
    diffs = []

    target_objs = get_objects(self)
    current_objs = get_objects(other)

    if not isinstance(target_objs, dict):
      target_objs = {label(obj): obj for obj in target_objs}
    if not isinstance(current_objs, dict):
      current_objs = {label(obj): obj for obj in current_objs}

    target_obj_names = set(target_objs)
    current_obj_names = set(current_objs)

    #self.log.debug("target_obj_names = {}".format(target_obj_names))
    #self.log.debug("current_obj_names = {}".format(current_obj_names))

    addobjs = target_obj_names - current_obj_names
    dropobjs = current_obj_names - target_obj_names

    # look for potential renames
    modify_diffs = []
    if rename:
      not_add = set()
      for add_name in addobjs:
        add_obj = target_objs[add_name]
        add_obj._ignore_name = True
        for drop_name in dropobjs:
          drop_obj = current_objs[drop_name]
          if add_obj == drop_obj:
            import pdb
            pdb.set_trace()
            modify_diffs.append(add_obj.rename(drop_obj))
            not_add.add(add_name)
            dropobjs.remove(drop_name)
            break
        add_obj._ignore_name = False
      addobjs.difference_update(not_add)

    pretty_type = ((target_objs and
                    type(next(iter(target_objs.values()))).pretty_type) or
                   (current_objs and
                    type(next(iter(current_objs.values()))).pretty_type) or
                   'Object')

    if addobjs:
      self.log.debug("  Adding {} {}s: {}".format(len(addobjs), pretty_type,
        ", ".join(target_objs[obj].pretty_name for obj in addobjs)))
      diffs.extend(
          other.add_subobjects(target_objs[addobj] for addobj in addobjs))
    if dropobjs:
      self.log.debug("  Dropping {} {}s: {}".format(len(dropobjs), pretty_type,
        ", ".join(current_objs[obj].pretty_name for obj in dropobjs)))
      diffs.extend(
          other.drop_subobjects(current_objs[dropobj] for dropobj in dropobjs))

    modify_diffs.extend(diff
        for target_obj in target_objs.values()
          if target_obj.name in current_objs
        for diff in target_obj.diff(current_objs[target_obj.name]))
    if modify_diffs:
      self.log.debug("  {} modifications for {}s".format(
        len(modify_diffs), pretty_type))
    diffs.extend(modify_diffs)

    return diffs

  def add_subobjects (self, subobjects):
    return [diff for obj in subobjects for diff in obj.create()]

  def drop_subobjects (self, subobjects):
    return [diff for obj in subobjects for diff in obj.drop()]

  def _depends_on (self, other, prop_name, integrity=Reference.HARD):
    old_dep = None
    if hasattr(self, prop_name):
      old_dep = getattr(self, prop_name)

    if old_dep != other:
      if old_dep:
        self._drop_dependency(old_dep)
      if other:
        self._set_dependency(other, integrity)

    setattr(self, prop_name, other)

  def _set_dependency (self, dep, integrity=Reference.HARD):
    if isinstance(dep, OracleObject):
      dep = [dep]
    self.log.debug("{} depends {} on [{}]".format(self.pretty_name, integrity,
      ", ".join(obj.pretty_name for obj in dep)))
    for obj in dep:
      ref = Reference(self, obj, integrity)
      self._dependencies.add(ref)
      #obj.referenced_by(self, integrity)
      obj._referenced_by.add(ref)

  def _drop_dependency (self, old_deps):
    if isinstance(old_deps, OracleObject):
      old_deps = [old_deps]
    self.log.debug("{} no longer depends on [{}]".format(self.pretty_name,
      ", ".join(old_dep.pretty_name for old_dep in old_deps)))
    remove_deps = set()
    for dep in self._dependencies:
      if dep.to in old_deps:
        remove_deps.add(dep)
        remove_refs = set()
        for ref in dep.to._referenced_by:
          #TODO:? if ref.from_ == self:
          if ref.from_ is self:
            remove_refs.add(ref)
        dep.to._referenced_by.difference_update(remove_refs)
    self._dependencies.difference_update(remove_deps)

  def _build_dep_set (self, get_objects, get_ref, test=lambda x: True):
    all = set()

    def recurse (_object):
      for ref in get_objects(_object):
        if test(ref):
          obj = get_ref(ref)
          if obj not in all and obj != self:
            all.add(obj)
            recurse(obj)

    recurse(self)
    return all

  def become (self, other_type):
    name = self.name
    self.__class__ = other_type
    self.__init__(name, reinit=True)

  @property
  def dependencies (self):
    return self._build_dep_set(lambda self: self._dependencies,
                               lambda ref: ref.to)

  def dependencies_with(self, integrity):
    return self._build_dep_set(lambda self: self._dependencies,
                               lambda ref: ref.to,
                               lambda ref: ref.integrity == integrity)

  @classmethod
  def from_db (class_, name=None, into_database=None):
    raise UnimplementedFeatureError(
      "Unimplemented from_db for {}".format(class_.__name__))
