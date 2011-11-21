import logging, pprint, inspect, itertools

from antlr3.ext import NamedConstant
from precog import db
from precog.errors import PrecogError
from precog.util import HasLog, progress_log

class Reference (object):
  SOFT = 'SOFT'
  HARD = 'HARD'
  AUTODROP = 'AUTODROP'

  def __init__ (self, from_, to, integrity=HARD):
    self.from_ = from_
    self.to = to
    self.integrity = integrity

  def __repr__ (self):
    return "<Reference from {} to {}, {}>".format(self.from_.pretty_name,
                                                  self.to.pretty_name,
                                                  self.integrity)
  def __str__ (self):
    return "{} has {} reference to {}".format(self.from_.pretty_name,
                                              self.integrity,
                                              self.to.pretty_name)

class Diff (object):
  COMMIT = 0
  DROP = 1
  CREATE = 2
  ALTER = 3
  NamedConstant.name(locals())

  def __init__ (self, sql, dependencies=None, produces=None, priority=None,
      terminator=';', binds=None):

    def make (t, x):
      if x is None:
        return t()
      if isinstance(x, t):
        return x
      if not isinstance(x, str):
        try:
          return t(x)
        except TypeError:
          pass
      return t((x,))

    self.sql = make(list, sql)
    stack = inspect.stack()
    self.created = []
    ininit = True
    for pop in stack:
      frame = inspect.getframeinfo(pop[0])
      if frame.function != '__init__':
        ininit = False
      if not ininit:
        self.created.append("{} line {}: {}".format(frame.filename,
          frame.lineno, frame.function))
      del frame
    del stack

    if produces is None and priority is None:
      priority = Diff.DROP
    elif priority is None:
      priority = Diff.ALTER
    self.priority = priority

    self.dropping = None
    if priority == Diff.DROP and dependencies:
      self.dropping = dependencies
      dependencies = None
    self._dependencies = make(set, dependencies)
    self.produces = make(set, produces)

    self.terminator = terminator
    self.binds = make(list, binds)

  def __repr__ (self):
    return "Diff({!r}, {!r}, {!r})".format(self.sql, self.dependencies,
        self.produces)

  def formatted (self, nosnip=False):
    binds = ''
    parts = []
    for sql, binds in itertools.zip_longest(self.sql, self.binds):
      if binds:
        parts.append("-- {}".format(", ".join(":{} = {}".format(col, val)
                                              for col,val in binds)))
      parts.append("".join((sql, self.terminator)))

    return "\n".join(parts)

  def __str__ (self):
    return self.formatted()

  def __eq__ (self, other):
    return self.sql == other.sql

  def __ne__ (self, other):
    return not self.sql == other.sql

  def __hash__ (self):
    return hash(tuple(self.sql))

  def apply (self):
    for sql, binds in itertools.zip_longest(self.sql, self.binds):
      db.execute(sql, **(binds or {}))

  @property
  def dependencies (self):
    other_deps = set()
    if self.produces:
      other_deps = {dep for product in self.produces
                    for dep in product.dependencies}
    elif self.dropping:
      other_deps = self.dropping.dependencies

    return (self._dependencies | other_deps) - self.produces

  def add_dependencies (self, others):
    try:
      self._dependencies.update(others)
    except TypeError:
      self._dependencies.add(others)

  @property
  def pretty_name (self):
    return "Diff {} {} {}".format(self.priority,
                                  self.sql if self.priority != Diff.CREATE
                                  else ", ".join(product.pretty_name
                                                 for product in self.produces),
                                  id(self))

class PlsqlDiff (Diff):

  def __init__ (self, sql, terminator='\n/', **kwargs):
    super().__init__(sql, terminator=terminator, **kwargs)

  def apply (self):
    super().apply()

    # log compile errors
    for product in self.produces:
      product.errors()

  def formatted (self, nosnip=False):
    parts = []
    for sql in self.sql:
      sqlparts = sql.split('\n')
      if not nosnip and len(sqlparts) > 10:
        sqlparts[1:-1] = ['  -- SNIP...']
      parts.extend(sqlparts)
      parts.append(self.terminator)

    return "\n".join(parts)

class Commit (Diff):

  def __init__ (self, dependencies):
    super().__init__('COMMIT', dependencies, priority=Diff.COMMIT)

def _edge_list (edges):
  return pprint.pformat({k.pretty_name: {dep.pretty_name for dep in v}
        for k,v in edges.items()})

class DiffCycleError (PrecogError):

  def __init__ (self, edges, visited):
    self.edges = edges
    self.visited = visited

  def __str__ (self):
    return "Diff cycle found:\nEdges:\n{}\nVisited:\n  {}".format(
        _edge_list(self.edges),
        "\n  ".join(v.pretty_name for v in self.visited))

class DuplicateCreationError (PrecogError):

  def __init__ (self, diff1, diff2):
    self.diff1 = diff1
    self.diff2 = diff2

  def __str__ (self):
    return "{} overlaps creation with {}".format(self.diff1, diff2)

def order_diffs (diffs):
  log = logging.getLogger('precog.diff.order_diffs')

  merged_diffs = {}
  for diff in progress_log(diffs, log, "Merging {} complete."):
    sql = tuple(diff.sql)
    if sql in merged_diffs:
      merged_diffs[sql].add_dependencies(diff._dependencies)
    else:
      merged_diffs[sql] = diff
  diffs = merged_diffs.values()

  # filter diffs to remove object drops that are autodropped by other diffs
  applicable_diffs = set(diffs)
  dropping = {diff.dropping: diff
              for diff in progress_log(diffs, log,
                                       "Gathering DROPs {} complete.")
              if diff.dropping}
  applicable_diffs = set()
  for diff in progress_log(diffs, log, "Filtering DROPs {} complete."):
    if diff.dropping:
      autodroppers = [obj for obj in diff.dropping.dependencies_with(
        Reference.AUTODROP) if obj in dropping]
      if autodroppers:
        if log.isEnabledFor(logging.DEBUG):
          log.debug(
            "Filtering {}: (Depends on {}) autodropped when dropping {}."
            .format(diff.pretty_name,
                    diff.dropping.dependencies_with(Reference.AUTODROP),
                    [a.pretty_name for a in autodroppers]))

        for d in autodroppers:
          # The other diff "produces" this diff
          dropping[d].produces.add(diff)
        continue
    applicable_diffs.add(diff)

  # Filter diffs to remove duplicate creates when a more encompassing statement
  # is creating the same thing as an individual one.
  creates = {}
  unnecessary_creates = set()
  for diff in progress_log(applicable_diffs, log,
                           "Filtering CREATEs {} complete."):
    if diff.priority == Diff.CREATE and diff.produces:
      for product in diff.produces:
        if product in creates:
          other_diff = creates[product]
          if other_diff.produces.issuperset(diff.produces):
            if log.isEnabledFor(logging.DEBUG):
              log.debug("Filtering {}, covered by {}".format(diff, other_diff))
            unnecessary_creates.add(diff)
            break;
          elif other_diff.produces.issubset(diff.produces):
            if log.isEnabledFor(logging.DEBUG):
              log.debug("Filtering {}, covered by {}".format(other_diff, diff))
            unnecessary_creates.add(other_diff)
          else:
            raise DuplicateCreationError(diff, other_diff)
        creates[product] = diff
  applicable_diffs.difference_update(unnecessary_creates)


  if log.isEnabledFor(logging.DEBUG):
    log.debug("All diffs:\n{}".format(pprint.pformat(
      {diff.pretty_name: {'sql': diff.sql,
                          'dependencies':
                            {dep.pretty_name for dep in diff._dependencies},
                          'produces': {product.pretty_name
                                       for product in diff.produces},
                          'dropping': diff.dropping and
                            diff.dropping.pretty_name,
                          'autodrop chain': diff.dropping and
                            {dep.pretty_name
                                for dep in diff.dropping
                                  .dependencies_with(Reference.AUTODROP)},
                          'created': diff.created
                         }
      for diff in diffs})))

  sort_by = (lambda x: x.priority + (10 if isinstance(x, PlsqlDiff) else 0)
             if isinstance(x, Diff) else 0)
  # edges is dict of obj: [dependencies, ...]
  edges = {}
  # Produced objects of diffs to be sorted
  S = sorted(applicable_diffs, key=sort_by)

  # create edge list
  def add_edge (from_, to):
    if from_ not in edges:
      edges[from_] = set()
    try:
      edges[from_].update(to)
    except TypeError:
      edges[from_].add(to)

  for diff in progress_log(diffs, log, "Edge list {} complete."):
    add_edge(diff, diff.dependencies)
    for product in diff.produces:
      add_edge(product, diff)

  for k,v in edges.items():
    edges[k] = sorted(v, key=sort_by)
  if log.isEnabledFor(logging.DEBUG):
    log.debug("Edge list:\n{}".format(_edge_list(edges)))

  # list of sorted diffs
  L = []
  visited = set()

  indent = ''
  def visit (node, this_visit=()):
    nonlocal indent
    cycle = False
    if node in this_visit:
      cycle = True
    this_visit += (node,)
    if cycle:
      raise DiffCycleError(edges, this_visit)

    if not node in visited:
      visited.add(node)

      # A diff may have been filtered out of diffs but remains for
      applicable = isinstance(node, Diff) and node in applicable_diffs
      if log.isEnabledFor(logging.DEBUG):
        if applicable:
          debugstr = "{}Can I apply {}?"
        else:
          debugstr = "{}Visiting {}"
        log.debug(debugstr.format(indent, node.pretty_name))

      if node in edges:
        for dependent in edges[node]:
          indent += '  '
          visit(dependent, this_visit)
          indent = indent[:-2]

      if applicable:
        if log.isEnabledFor(logging.DEBUG):
          log.debug("{}Apply {}".format(indent, node.pretty_name))
        L.append(node)

  for node in progress_log(S, log, "Ordering {} complete."):
    visit(node)

  return L
