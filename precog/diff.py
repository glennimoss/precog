from copy import copy
from precog.errors import PrecogError

class Diff (object):

  def __init__ (self, sql, dependencies={}, produces=None):
    self.sql = sql
    if not isinstance(dependencies, set):
      dependencies = {dependencies}
    self.dependencies = dependencies
    self.produces = produces

  def __repr__ (self):
    return "Diff({!r}, {!r}, {!r})".format(self.sql, self.dependencies,
        self.produces)

  def __str__ (self):
    return self.sql

class DiffCycleError (PrecogError):
  pass

def order_diffs (diffs):
  diffs = {diff.produces or diff: diff for diff in diffs}
  # list of obj: [dependencies, ...]
  #edges = {obj: diff.dependencies for obj, diff in diffs.items()}
  edges = {}
  # Produced objects of diffs to be sorted
  S = diffs.keys()

  # create edge list
  for obj, diff in diffs.items():
    if diff.dependencies:
      if obj not in edges:
        edges[obj] = set()
      else:
        print("I don't think this should happen....")

      edges[obj].update(diff.dependencies)

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
