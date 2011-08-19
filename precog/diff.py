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
      terminator=';'):
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
      if produces is not None:
        dependencies = produces.dependencies
      else:
        dependencies = set()
    if not isinstance(dependencies, set) and not isinstance(dependencies, list):
      dependencies = {dependencies}
    self.dependencies = dependencies
    self.produces = produces

    if produces is None and priority is None:
      priority = Diff.DROP
    elif priority is None:
      priority = Diff.ALTER
    self.priority=priority

    self.terminator = terminator

  def __repr__ (self):
    return "Diff({!r}, {!r}, {!r})".format(self.sql, self.dependencies,
        self.produces)

  def __str__ (self):
    return self.sql + self.terminator

  def apply (self):
    return db.execute(self.sql)

  @property
  def pretty_name (self):
    pretty_deps = [dep.pretty_name for dep in self.dependencies
        if not isinstance(dep, Diff)]
    return "Diff {} [{}]".format(self.priority,
        self.produces.pretty_name if self.produces
        else self.sql if self.priority == Diff.DROP else ", ".join(pretty_deps))

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

  diffs = {diff.produces or diff: diff for diff in diffs if diff}
  log.debug("All diffs:\n{}".format(pprint.pformat(
    {label.pretty_name: {'sql': diff.sql,
                        'dependencies':
                          set(dep.pretty_name for dep in diff.dependencies),
                        'produces': diff.produces and diff.produces.pretty_name,
                        'created': diff.created
                       }
    for label, diff in diffs.items()})))

  # list of obj: [dependencies, ...]
  edges = {}
  # Produced objects of diffs to be sorted
  S = [node for node, devnull in
      sorted(diffs.items(), key=lambda x: x[1].priority)]

  # create edge list
  for obj, diff in diffs.items():
    if diff.dependencies:
      if obj not in edges:
        edges[obj] = set()
      else:
        print("I don't think this should happen....")

      edges[obj].update(diff.dependencies)

  for k,v in edges.items():
    edges[k] = sorted(v, key=lambda x: diffs[x].priority if x in diffs else 0)
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
      if node in diffs:
        log.debug("Can I apply {}?".format(diffs[node].pretty_name))
      else:
        log.debug("Visiting {}".format(node.pretty_name))

      if node in edges:
        for dependent in edges[node]:
          visit(dependent, this_visit)

      if node in diffs:
        log.debug("Apply {}".format(diffs[node].pretty_name))
        L.append(diffs[node])

  for node in S:
    visit(node)

  return L
