from intervaltree import IntervalTree
from .taskunit import TaskUnit
from .taskunitpriorityqueue import TaskUnitPriorityQueue
from .exceptions import DuplicateTaskException
from .period import Period


class Conflict(object):
  """
    A data structure that holds all tasks that conflict at a given time.
  """
  def __init__(self, intervals):
    self._intervals = list(intervals)


  @property
  def period(self):
    begin = self._intervals[0].begin
    end = self._intervals[0].end
    for interval in self._intervals:
      # get the earliest begin time
      if interval.begin < begin:
        begin = interval.begin
      # get the earliest begin time
      if interval.end > end:
        end = interval.end
    return Period(begin, end)


  def __iter__(self):
    return iter(self._intervals)


  def __str__(self):
    string = "Conflicts: <"
    for interval in self._intervals:
      string += str(interval)
    string += ">"
    return string


  def __len__(self):
    return len(self._intervals)




class ConflictSet(object):
  """
    A data structure to hold all conflicts for a given task set.
  """
  def __init__(self, conflicts):
    self._conflicts = list(conflicts)


  def all(self):
    return self._conflicts


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


  def asDict(self):
    conflicts = []
    for conflict in self._conflicts:
      intervals = []
      for interval in conflict:
        _interval = {}
        begin = interval.begin.isoformat()
        end = interval.end.isoformat()
        _interval["begin"] = begin
        _interval["end"] = end
        intervals.append(_interval)
      conflicts.append(intervals)
    return conflicts


  def __str__(self):
    string = ""
    for conflict in self._conflicts:
      string += str(conflict) + "\n"
    return string


class TaskSet(object):
  """
    Holds a set of tasks in a priority queue.
  """
  def __init__(self):
    self._tasksQueue = TaskUnitPriorityQueue() # keep r1 < r2 < r3 order.
    self._intervalTree = IntervalTree()

  @property
  def tasks(self):
    return self._tasksQueue.items()


  def add(self, task):
    if isinstance(task, TaskUnit):
      if not self._tasksQueue.contains(task.taskID):
        self._addTaskToTree(task)
        self._tasksQueue.push(task)
      else:
        raise DuplicateTaskException
    else:
      raise TypeError("Expected %s got %s" % (TaskUnit, type(task)))


  def _addTaskToTree(self, task):
    """
      Adds task to interval tree.
    """
    self._intervalTree.addi(
      begin=task.release,
      end=task.deadline,
      data=task.taskID
    )


  def remove(self, taskID):
    """
      Removes a task from the set and returns it.
    """
    task = self._tasksQueue.remove(taskID)
    self._intervalTree.discardi(task.release, task.deadline, task.taskID)
    return task


  def findConflicts(self):
    """
      Finds all the conflicts within the tasks set.
      A conflict being, any two or more tasks that need
      to be proccessed at some point simultaneously.
      In terms of an interval tree, the two task times 'overlap'.

      This method finds all the conflicts of the current task set
      held by this class.
    """
    begin = self._intervalTree.begin()
    end = self._intervalTree.end()
    conflicts = []
    conflictObjs = []
    intervals = sorted(self._intervalTree[begin:end])
    for interval in intervals:
      _intervals = self._intervalTree[interval.begin:interval.end]
      if len(_intervals) > 1: # theres a conflict
        if _intervals not in conflicts:
          conflicts.append(_intervals)
          conflictObjs.append(Conflict(_intervals))
    return ConflictSet(conflictObjs)


  def findNonConflicts(self):
    """
    Finds all the tasks that do not conflict with any other tasks.
    """
    conflicts = self.findConflicts().flatten()
    return self._intervalTree.difference(conflicts).items()


  def __iter__(self):
    return self._tasksQueue
