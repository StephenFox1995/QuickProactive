from orderpriority import OrderPriorityQueue
from priorityworker import PriorityWorker

class PriorityService(object):
  def __init__(self, orderDBConn):
    self._orderDBConn = orderDBConn
    self.__workers = {}
  
  def new(self, business, refresh=5000):
    """
      Creates a new priorityworker.PriorityWorker to periodically
      calculate the priority of new orders.
    """
    pQueue = OrderPriorityQueue()
    pWorker = PriorityWorker(business, self._orderDBConn, pQueue, refresh=refresh)
    self.__workers["businessID"] = pWorker
    pWorker.run()
    
   
