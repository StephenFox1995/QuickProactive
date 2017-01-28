from .taskunitpriorityqueue import TaskUnitPriorityQueue
from .priorityworker import PriorityWorker

class PriorityService(object):
  def __init__(self, orderDBConn):
    self._orderDBConn = orderDBConn
    self.__workers = {}

  def newWorker(self, business, workerID, refresh=5000):
    """
      Creates a new priorityworker.PriorityWorker to periodically
      calculate the priority of new orders.

      @param business:(object) Object that contains 'businessID'
      @param refresh:(int)  The refresh rate in milliseconds, i.e
                            how often the service will run.
    """
    pQueue = TaskUnitPriorityQueue()
    pWorker = PriorityWorker(business, self._orderDBConn, pQueue, refresh=refresh)
    self.__workers[workerID] = pWorker
    pWorker.run()

  def stopWorker(self, workerID):
    return self.__workers[workerID]
