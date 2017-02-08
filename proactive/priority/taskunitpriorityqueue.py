import heapq as heap
from copy import copy
from .priority import Priority

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
