import logging

from precog import db
from precog.errors import PlsqlSyntaxError, PrecogError
from precog.util import HasLog

class Diff (object):
  DROP = 1
  CREATE = 2
  ALTER = 3

  def __init__ (self, sql, dependencies=None, produces=None, priority=None,
      terminator=';'):
    self.sql = sql

    if dependencies is None and produces is not None:
      dependencies = produces.dependencies
    if not isinstance(dependencies, set):
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

class PlsqlDiff (HasLog, Diff):

  def apply (self):
    super().apply()

    # log compile errors
    self.produces.errors()

class DiffCycleError (PrecogError):
  pass

def order_diffs (diffs):
  log = logging.getLogger('precog.diff.order_diffs')

  diffs = {diff.produces or diff: diff for diff in diffs if diff}
  #log.debug('Diffs:')
  #for k,v in diffs.items():
    #log.debug("  {} {}: depends on {}".format(type(k).__name__,
      #k.sql if isinstance(k, Diff) else k.name,
      #", ".join(dep.pretty_name for dep in v.dependencies) or 'nothing'))

  # list of obj: [dependencies, ...]
  #edges = {obj: diff.dependencies for obj, diff in diffs.items()}
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

  log.debug('Edge list:')
  for k,v in edges.items():
    edges[k] = sorted(v, key=lambda x: diffs[x].priority if x in diffs else 0)
    log.debug("  {} {} -> {}".format(type(k).__name__,
      k.sql if isinstance(k, Diff) else k.name,
      ", ".join(dep.pretty_name for dep in v)))

  # list of sorted diffs
  L = []
  visited = set()

  def visit (node, this_visit=()):
    cycle = False
    if node in this_visit:
      cycle = True
    this_visit += (node,)
    if cycle:
      raise DiffCycleError("Cycle found in diff list {}".format(this_visit))

    if not node in visited:
      visited.add(node)

      if node in edges:
        for dependent in edges[node]:
          visit(dependent, this_visit)

      if node in diffs:
        L.append(diffs[node])

  for node in S:
    visit(node)

  return L
