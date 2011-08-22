import logging, pprint, inspect

from antlr3.ext import NamedConstant
from precog import db
from precog.errors import PlsqlSyntaxError, PrecogError
from precog.util import HasLog

class Diff (object):
  COMMIT = 0
  DROP = 1
  CREATE = 2
  ALTER = 3
  NamedConstant.name(locals())

  def __init__ (self, sql, dependencies=None, produces=None, priority=None,
      terminator=';', binds={}):
    self.sql = sql
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

    if dependencies is None:
      dependencies = set()
    if isinstance(dependencies, list):
      dependencies = set(dependencies)
    if not isinstance(dependencies, set):
      dependencies = {dependencies}
    self._dependencies = dependencies
    self.produces = produces

    if produces is None and priority is None:
      priority = Diff.DROP
    elif priority is None:
      priority = Diff.ALTER
    self.priority=priority

    self.terminator = terminator
    self.binds = binds

  def __repr__ (self):
    return "Diff({!r}, {!r}, {!r})".format(self.sql, self.dependencies,
        self.produces)

  def __str__ (self):
    binds = ''
    if self.binds:
      binds = "-- {}\n".format(", ".join(":{} = {}".format(col, val)
                                       for col,val in self.binds.items()))
    return binds + self.sql + self.terminator

  def apply (self):
    return db.execute(self.sql, **self.binds)

  @property
  def dependencies (self):
    return self._dependencies | (self.produces.dependencies
                                 if self.produces else set())

  @property
  def pretty_name (self):
    pretty_deps = [dep.pretty_name for dep in self.dependencies
        if not isinstance(dep, Diff)]
    return "Diff {} [{}] {}".format(self.priority,
        self.produces.pretty_name if self.produces
        else self.sql if self.priority == Diff.DROP else ", ".join(pretty_deps),
        id(self))

class PlsqlDiff (Diff):

  def __init__ (self, sql, dependencies=None, produces=None, priority=None,
      terminator='\n/'):
    super().__init__(sql, dependencies, produces, priority, terminator)

  def apply (self):
    super().apply()

    # log compile errors
    self.produces.errors()

class Commit (Diff):

  def __init__ (self, dependencies):
    super().__init__('COMMIT', dependencies, priority=Diff.COMMIT)

def _edge_list (edges):
  return pprint.pformat({k.pretty_name: set(dep.pretty_name for dep in v)
        for k,v in edges.items()})

class DiffCycleError (PrecogError):

  def __init__ (self, edges, visited):
    self.edges = edges
    self.visited = visited

  def __str__ (self):
    return "Diff cycle found:\nEdges:\n{}\nVisited:\n  {}".format(
        _edge_list(self.edges),
        "\n  ".join(v.pretty_name for v in self.visited))

def order_diffs (diffs):
  log = logging.getLogger('precog.diff.order_diffs')

  log.debug("All diffs:\n{}".format(pprint.pformat(
    {diff.pretty_name: {'sql': diff.sql,
                        'dependencies':
                          set(dep.pretty_name for dep in diff._dependencies),
                        'produces': diff.produces and diff.produces.pretty_name,
                        'created': diff.created
                       }
    for diff in diffs})))

  # list of obj: [dependencies, ...]
  edges = {}
  # Produced objects of diffs to be sorted
  S = sorted(diffs, key=lambda x: x.priority)

  # create edge list
  def add_edge (from_, to):
    if from_ not in edges:
      edges[from_] = set()
    try:
      edges[from_].update(to)
    except TypeError:
      edges[from_].add(to)

  for diff in diffs:
    add_edge(diff, diff.dependencies)
    if diff.produces:
      add_edge(diff.produces, diff)

  for k,v in edges.items():
    edges[k] = sorted(v, key=lambda x: x.priority if isinstance(x, Diff) else 0)
  log.debug("Edge list:\n{}".format(_edge_list(edges)))

  # list of sorted diffs
  L = []
  visited = set()

  def visit (node, this_visit=()):
    cycle = False
    if node in this_visit:
      cycle = True
    this_visit += (node,)
    if cycle:
      raise DiffCycleError(edges, this_visit)

    if not node in visited:
      visited.add(node)
      if isinstance(node, Diff):
        log.debug("Can I apply {}?".format(node.pretty_name))
      else:
        log.debug("Visiting {}".format(node.pretty_name))

      if node in edges:
        for dependent in edges[node]:
          visit(dependent, this_visit)

      if isinstance(node, Diff):
        log.debug("Apply {}".format(node.pretty_name))
        L.append(node)

  for node in S:
    visit(node)

  return L
