from intervaltree import IntervalTree
from datetime import datetime


def tasksInRange(tasks, start, end):
  taskRange = []
  for task in tasks:
    if task["release"] >= start and task["deadline"] <= end:
      taskRange.append(task)
  return taskRange

def assignworkers(tasks, m, start, end):
  starttime = 09.00
  endtime = 18.00
  tasks = tasksInRange(tasks, starttime, endtime)
  tree = IntervalTree()

  for task in tasks:
    tree.addi(begin=task["release"], end=task["deadline"], data=task["id"])

  start = tree.begin()
  end = tree.end()
  intervals = sorted(tree[start:end])
  conflicts = []

  for x in intervals:
    t = tree[x.begin:x.end]
    if t > 1:
      if t not in conflicts:
        conflicts.append(t)
  for x in conflicts:
    print(x)

  # for interval in tree:
  #   if tree.overlaps(interval.begin, interval.end):
  #     print(tree.search(interval.begin, interval.end))
  #   print(tree.overlaps(interval.begin, interval.end))
  # Query tree to find all conflicts that occur until closing time.
  # print(tree.overlaps(starttime, endtime))

  # task = tasks[0] # take the first task.
  # for x in range(1, len(tasks)) # find any tasks that conflict with this task up to m
  #   conflicts = tree[tasks[0]["release"]: tasks[0]["deadline"]
  #   if conflicts >= m:







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
  ]
  assignworkers(tasks, 2, 9.34, 10)


