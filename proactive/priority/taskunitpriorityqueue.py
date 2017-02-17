import heapq as heap
from copy import copy
from .priority import Priority
from .exceptions import UnkownTaskException

class TaskUnitPriorityQueue(object):
  def __init__(self, items=None):
    self._pQueue = []
    if items != None:
      if not isinstance(items, list):
        raise TypeError("items arg should be of type list")
      # Check that all types are in Prioritized sub tree.
      [all(isinstance(i, Priority) for i in items)]
      self.push(items)

  def __iter__(self):
    return self


  def next(self):
    try:
      return heap.heappop(self._pQueue)
    except IndexError:
      raise StopIteration


  def remove(self, taskID):
    """
      Removes a task from the priority queue at some index and returns it.
    """
    if self.contains(taskID):
      return self._remove(taskID)
    else:
      raise UnkownTaskException


  def _remove(self, taskID):
    for task in self._pQueue:
      if task.taskID == taskID:
        self._pQueue.remove(task)
        heap.heapify(self._pQueue)
        return task


  def push(self, obj):
    if isinstance(obj, list):
      for i in obj:
        heap.heappush(self._pQueue, i)
    elif isinstance(obj, Priority):
      heap.heappush(self._pQueue, obj)


  def pop(self):
    return heap.heappop(self._pQueue)


  def popAll(self):
    allElements = []
    for _ in range(0, self.count()):
      allElements.append(self.pop().asDict())
    return allElements


  def contains(self, taskID):
    """
      Checks to see if the priority queue contains a task.
    """
    for t in self._pQueue:
      if t.taskID == taskID:
        return True
    return False


  def count(self):
    return len(self._pQueue)


  def printQueue(self):
    for i in self._pQueue:
      print(i.asDict())


  def items(self):
    return copy(self._pQueue)


  def __dict__(self):
    _dict = {"queue": []}
    for i in self._pQueue:
      _dict["queue"].append(i.asDict())
    return _dict
