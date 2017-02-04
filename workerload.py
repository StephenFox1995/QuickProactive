from intervaltree import IntervalTree
from datetime import datetime
import itertools

def findConflicts(tree, threshold):
  begin = tree.begin()
  end = tree.end()
  conflicts = []
  # Get all tasks that are currently in the tree, which
  # do not have worker assigned to them.
  intervals = sorted(tree[begin:end])
  intervalsOverThreshold = []
  for interval in intervals:
    intervalConflicts = tree[interval.begin:interval.end] # find all conflicts with this task.
    if intervalConflicts > 1:
      if intervalConflicts not in conflicts:
        conflicts.append(intervalConflicts)
    else:
      if intervalConflicts not in intervalsOverThreshold:
        intervalsOverThreshold.append(intervalConflicts)
  return (conflicts, intervalsOverThreshold)

def nonConflicts(tree, conflicts):
  return IntervalTree(conflicts) - tree

def makeTree(tasks):
  tree = IntervalTree()
  for task in tasks:
    tree.addi(begin=task["release"], end=task["deadline"], data=task["id"])
  return tree

def flatten(s):
  items = []
  for x in s:
    for y in x:
      items.append(y)
  return items




if __name__ == "__main__":
# T1 9.30 - 10.00,
# T2 9.40-11.00
# T3 11.30 - 12.00
# T4 11.35 - 12.00
# T5 11.50 - 12.00

  workers = [
    {"id": 1, "assignedTasks": []},
    {"id": 2, "assignedTasks": []}
  ]
  tasks = [
    {"id": "t1", "release": 9.30, "deadline": 10.00, "status": "unassigned"},
    {"id": "t2", "release": 9.40, "deadline": 11.00, "status": "unassigned"},
    {"id": "t3", "release": 11.30, "deadline": 12.00, "status": "unassigned"},
    {"id": "t4", "release": 11.35, "deadline": 12.00, "status": "unassigned"},
    {"id": "t5", "release": 11.50, "deadline": 12.30, "status": "unassigned"},
    {"id": "t6", "release": 14.50, "deadline": 15.30, "status": "unassigned"},
  ]
  tree = makeTree(tasks)
  conflicts = findConflicts(tree, 1)
  conflicts = flatten(conflicts[0])

  # flatten intervals array
  # x = list(itertools.chain.from_iterable(conflictingIntervals))
  # for _ in x:
  #   print(_)
  nonConflictingTasks = nonConflicts(tree, conflicts)
  print(nonConflictingTasks)
  # for _ in conflictingIntervals[0]:
  #   print(_)
  # for _ in conflictingIntervals[1]:
  #   print(_)
