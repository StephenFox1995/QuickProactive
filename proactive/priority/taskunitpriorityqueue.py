import heapq as heap
from .priority import Priority

class TaskUnitPriorityQueue(object):
  def __init__(self, items=None):
    self._pQueue = []
    if items != None:
      if not isinstance(items, list):
        raise TypeError("items arg should be of type list")
      # Check that all types are in Prioritized sub tree.
      [all(isinstance(i, Priority) for i in items)]
      self.add(items)


  def add(self, obj):
    if isinstance(obj, list):
      [heap.heappush(self._pQueue, i) for i in obj]
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

  def asDict(self):
    _dict = {"queue": []}
    for i in self._pQueue:
      _dict["queue"].append(i.asDict())
    return _dict
