import logging
from pprint import pprint, pformat

from precog import db
from precog.errors import PrecogError

class Diff (object):
  DROP = 1
  CREATE = 2
  ALTER = 3

  def __init__ (self, sql, dependencies=set(), produces=None, priority=None):
    self.sql = sql
    if not isinstance(dependencies, set):
      dependencies = {dependencies}
    self.dependencies = dependencies
    self.produces = produces

    if produces is None and priority is None:
      priority = Diff.DROP
    elif priority is None:
      priority = Diff.ALTER
    self.priority=priority

  def __repr__ (self):
    return "Diff({!r}, {!r}, {!r})".format(self.sql, self.dependencies,
        self.produces)

  def __str__ (self):
    return self.sql

  def apply (self):
    return db.execute(self.sql)

class DiffCycleError (PrecogError):
  pass

def order_diffs (diffs):
  log = logging.getLogger('precog.diff.order_diffs')

  diffs = {diff.produces or diff: diff for diff in diffs if diff}
  log.debug('Diffs:')
  #for k,v in diffs.items():
    #log.debug("  {}: {} depends on {}".format(
      #k.sql if isinstance(k, Diff) else k.name, v.sql,
      #", ".join(str(dep.name) for dep in v.dependencies)))

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
    #log.debug("  {} -> {}".format(
      #k.sql if isinstance(k, Diff) else k.name,
      #", ".join(str(dep.name) for dep in v)))

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
