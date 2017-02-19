from intervaltree import IntervalTree
from .taskunit import TaskUnit
from .taskunitpriorityqueue import TaskUnitPriorityQueue
from .exceptions import DuplicateTaskException
from .conflict import Conflict, ConflictSet


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
    if not self._tasksQueue.contains(task.taskID):
      self._addTaskToTree(task)
      self._tasksQueue.push(task)
    else:
      raise DuplicateTaskException


  def _addTaskToTree(self, task):
    """
      Adds task to interval tree.
    """
    self._intervalTree.addi(
      begin=task.release,
      end=task.deadline,
      data=task.taskID
    )


  def remove(self, task):
    self._intervalTree.discardi(task.release, task.deadline, task.taskID)
    self._tasksQueue.remove(task.taskID)


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
    nonConflictObjs = []
    intervals = sorted(self._intervalTree[begin:end])
    for interval in intervals:
      _intervals = self._intervalTree[interval.begin:interval.end]
      if len(_intervals) > 1: # theres a conflict
        if _intervals not in conflicts:
          conflicts.append(_intervals)
          conflictObjs.append(Conflict(_intervals))
      else:
        nonConflictObjs.append(Conflict(_intervals))
    return ConflictSet(conflictObjs), ConflictSet(nonConflictObjs)


  def __iter__(self):
    return self._tasksQueue
