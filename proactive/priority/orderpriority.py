import heapq as heap
from prioritized import Prioritized
import json

class OrderPriorityQueue(object):
  def __init__(self, items=None):
    self._pQueue = []
    if items != None:
      if type(items) is not list:
        raise TypeError("items arg should be of type list")
      # Check that all types are in Prioritized sub tree.
      [(isinstance(i, Prioritized) for i in items)]
      self.add(items)


  def add(self, obj):
    if type(obj) is list:
      [heap.heappush(self._pQueue, i) for i in obj]
    elif isinstance(obj, Prioritized):
      heap.heappush(self._pQueue, obj)
  
  def pop(self):
    return heap.heappop(self._pQueue)

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