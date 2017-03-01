from intervaltree import IntervalTree
from .taskunit import TaskUnit
from .taskunitpriorityqueue import TaskUnitPriorityQueue
from .exceptions import DuplicateTaskException
from .conflict import Conflict, ConflictSet
from datetime import datetime

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


  def _findLatestInterval(self, intervals):
    """
      Find the latest interval.
    """
    latest = intervals[0]
    for interval in intervals:
      if interval.begin > latest.begin:
        latest = interval
    return latest

  def _orIntervals(self, intervalListA, intervalListB):
    return list(set(intervalListA) | set(intervalListB))

  def _conflictPath(self, interval, intervalTree):
    """
      @param interval The interval to find conflicts with.
      @param intervalTree The intervalTree that contains all intervals
    @param exclude Any intervals to exclude from conflict detection.
      Finds the longest number of intervals that are all overlapping (conflicting).
        For example:
          if A and B conflict and B and C conflict and A is the
          interval we're looking for conflicts with, the returned
          intervals will be A, B, C.
        Another example:
          if D and E conflict and F and G conflict, and we're looking
          for all conflicts with D, only D and E will be returned as
          F and G are not overlapping with either D and E.
    """
    intervals = list(intervalTree.search(interval))
    # if only one interval, check if its the one we're
    # trying to find conflicts with.
    if len(intervals) == 1 and intervals[0] == interval:
      return []
    # now find the latest of all the intervals and get all conflicts
    # with and keep going until there are no more conflicts.
    latestInterval = self._findLatestInterval(intervals)
    # remove all the conflicts, we dont need to check them again.
    intervalTree.remove_overlap(interval)
    # put the latest conflict back into the tree and find its conflicts
    intervalTree.add(latestInterval)
    # now go find all conflicts with the latest interval until there are none.
    return self._orIntervals(intervals, self._conflictPath(latestInterval, intervalTree))


  def _intervalConflictAlreadyDetected(self, interval, conflicts):
    """
      Checks to see if interval was already detected to conflict.
    """
    for conflict in conflicts:
      for ival in conflict:
        if ival == interval:
          return True
    return False


  def findConflicts(self):
    """
      Finds all conflicts within the task set.
    """
    begin = self._intervalTree.begin()
    end = self._intervalTree.end()
    conflicts = []
    conflictObjs = []
    nonConflictsObjs = []
    intervals = sorted(self._intervalTree[begin:end])
    for interval in intervals:
      # check if this interval was already detected to conflict
      if self._intervalConflictAlreadyDetected(interval, conflicts):
        continue
      conflictIntervals = self._conflictPath(interval, self._intervalTree.copy())
      if len(conflictIntervals) > 0: # there was a  conflict
        conflicts.append(conflictIntervals)
        conflictObjs.append(Conflict(conflictIntervals))
      else:
        nonConflictsObjs.append(Conflict(interval))
    return ConflictSet(conflictObjs), ConflictSet(nonConflictsObjs)


  def __iter__(self):
    return self._tasksQueue
