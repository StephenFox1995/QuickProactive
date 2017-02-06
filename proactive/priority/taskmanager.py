from datetime import datetime
from intervaltree import IntervalTree
from .exceptions import LateDeadlineException

class ConflictSet(object):
  def __init__(self, conflicts):
    self._conflicts = conflicts

  def allLessThanOrEqual(self, value):
    conflicts = []
    for conflict in self._conflicts:
      if len(conflict) <= value:
        conflicts.append(conflict)
    return conflicts

  def allGreaterThan(self, value):
    conflicts = []
    for conflict in self._conflicts:
      if len(conflict) > value:
        conflicts.append(conflict)
    return conflicts

  def max(self):
    maxConflict = None
    maxSize = 0
    for conflict in self._conflicts:
      if len(conflict) > maxSize:
        maxConflict = conflict
        maxSize = len(conflict)
    return maxConflict

  def flatten(self):
    intervals = []
    for x in self._conflicts:
      for y in x:
        intervals.append(y)
    return intervals



class TaskManager(object):
  def __init__(self, period):
    self.__tasks = []
    self.__intervalTree = IntervalTree()
    self.__workers = []
    if isinstance(period[0], datetime) and isinstance(period[1], datetime):
      self.__start = period[0]
      self.__end = period[1]
    else:
      raise TypeError(
        "period[0] and period[1] should be datetime instances."
      )

  @property
  def tasks(self):
    return self.__tasks

  def addWorker(self, worker):
    self.__workers.append(worker)

  def addTask(self, task):
    if task.deadline > self.__end:
      raise LateDeadlineException(
        "Cannot process this task as it's deadline is %s is after %s"
        % (task.deadline, self.__end)
      )
    self.__tasks.append(task)
    self.__addTaskToTree(task)

  def addTasks(self, tasks):
    for task in tasks:
      self.__tasks.append(task)
      self.__addTaskToTree(task)

  def __addTaskToTree(self, task):
    self.__intervalTree.addi(
      begin=task.release,
      end=task.deadline,
      data=task.taskID
    )

  def findConflicts(self):
    """
      Finds all the conflicts within the tasks set.
      A conflict being, any two or more tasks that need
      to be proccessed at some point simultaneously.
      In terms of an interval tree, the two task times 'overlap'.

      This method finds all the conflicts of the current task set
      held by this class.
    """
    begin = self.__intervalTree.begin()
    end = self.__intervalTree.end()
    conflicts = []
    intervals = sorted(self.__intervalTree[begin:end])
    for interval in intervals:
      _intervals = self.__intervalTree[interval.begin:interval.end]
      if len(_intervals) > 1: # theres a conflict
        if _intervals not in conflicts:
          conflicts.append(_intervals)
    return ConflictSet(conflicts)

  def findNonConflicts(self):
    conflicts = self.findConflicts().flatten()
    return self.__intervalTree.difference(conflicts).items()

  def highestNumberOfWorkersNeeded(self, multitask=1):
    """
      Calculates the highest number of employees needed
      to service the tasks set.
      @param multitask:(int) The maximum amount of tasks a single
        worker can complete at any given time simultaneously.
    """
    conflict = self.findConflicts().max()
    return self.workersNeeded(len(conflict), multitask)

  def workersNeeded(self, k, m):
    """
      Calculates the number of employees needed to deal with a conflict.
      @param k:() The number of conflicts
      @param m:() The highest number of tasks employees can service simultaneously.
    """
    # formula: k/m
    from math import ceil
    return ceil(float(k)/float(m))

