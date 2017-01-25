from ..config import Configuration
from ..travel import Travel

class PriorityWorker(object):
  def __init__(self, business, ordersDBConn, queue, refresh=5000):
    pass
    """
      @param ordersDBConn:(db.prioritydb.PriorityDB) Database connection to read orders from.
      
      @param businessID:(str) The id of the business.

      @param queue:(orderpriority.OrderPriorityQueue) A OrderPriorityQueue instance.

      @param refresh:(int) - milliseconds: How often the database should be read to when checking
        for new orders. How often the database should be written to with the current state of the
        priority queue.
    """

    self._coordinates = business["coordinates"]
    self._businessID =  business["id"]
    
    self.ordersDBConn = ordersDBConn
    self._queue = queue
    self._config = Configuration()
    self._travel = Travel(gmapsKey=self._config.read([Configuration.GMAPS_KEY])[0])
  
  def __readOrders(self):
    # TODO: only get orders that have not been delivered.
    orders = self.ordersDBConn.orders.find({"businessID": self._businessID})

  def begin(self):
    self._loop()

  def _loop(self):
    orders = self.__readOrders()
    for order in orders:
      pass
      # deadline = self._calculateCustomerArrivalTime(order)

  def _calculateCustomerArrivalTime(self, order):
    lat = order["coordinates"]["lat"]
    lng = order["coordinates"]["lng"]
    travel.find(businessLocation, testlocation1, metric.DURATION, measure="value")
    self._travel.find()

  def _calculateCustomerDistance(self, order):
    pass
    


