from ..config import Configuration
from ..travel import Travel, coord, metric

class PriorityWorker(object):
  def __init__(self, business, ordersDBConn, queue, refresh=5000):
    """
      @param ordersDBConn:(db.prioritydb.PriorityDB) Database connection to read orders from.

      @param businessID:(str) The id of the business.

      @param queue:(orderpriority.OrderPriorityQueue) A OrderPriorityQueue instance.

      @param refresh:(int) - milliseconds: How often the database should be read to when checking
        for new orders. How often the database should be written to with the current state of the
        priority queue.
    """
    self._businessCoordinates = business["coordinates"]
    self._businessID = business["id"]
    self._ordersDBConn = ordersDBConn
    self._queue = queue
    self._refresh = refresh
    self._config = Configuration()
    self._travel = Travel(gmapsKey=self._config.read([Configuration.GMAPS_KEY])[0])

  def __readUnprocessedOrders(self):
    return self._ordersDBConn.read(self._businessID)


  def run(self):
    self._loop()


  def _loop(self):
    orders = self.__readUnprocessedOrders()
    for order in orders:
      print(order)
      deadline = self._calculateCustomerArrivalTime(order)


  def _calculateCustomerArrivalTime(self, order):
    lat = order["coordinates"]["lat"]
    lng = order["coordinates"]["lng"]
    customerCoordinates = coord.coordinate(lat, lng)
    return self._travel.find(
      self._businessCoordinates,
      customerCoordinates,
      metric.DURATION,
      measure="value"
    )

  def _calculateCustomerDistance(self, order):
    pass
