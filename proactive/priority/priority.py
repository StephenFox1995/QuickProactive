import heapq as heap
from prioritized import Prioritized

class Priority(object):
  def __init__(self, items=None, threshold=None):
    if type(items) is not list:
      raise TypeError("items arg should be of type list")
    # Check that all types are in Prioritized sub tree.
    [all(isinstance(i, Prioritized) for i in items)]
    self._queue = []
    self.add(items)

  def add(self, items):
    [heap.heappush(self._queue, i) for i in items]
    heap.heapify(self._queue)
  
  def pop(self):
    return heap.heappop(self._queue)

  def printQueue(self):
    for i in self._queue:
      print(i.processing)


    

    
    