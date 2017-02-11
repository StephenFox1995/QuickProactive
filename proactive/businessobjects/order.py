from .dataitem import DataItem

class Order(DataItem):
  class Status(object):
    UNPROCESSED = "unprocessed"
    PROCESSED = "processed"

  def __init__(self, orderID, status, processing, customerCoordinates, createdAt, cost):
    """
      @param orderID:(str) The id of the order.
      @param profit:(double) The profit from this order.
      @param customerCoordinates:(object) Contains coordinates such as {"lat": x, "lng": y}
    """
    self._orderID = orderID
    self._status = status
    self._processing = processing
    self._customerCoordinates = customerCoordinates
    self._cost = cost
    self._createdAt = createdAt

  @property
  def orderID(self):
    return self._orderID

  @property
  def status(self):
    return self._status

  @property
  def processing(self):
    return self._processing

  @property
  def customerCoordinates(self):
    return self._customerCoordinates

  @property
  def cost(self):
    return self._cost

  @property
  def createdAt(self):
    return self._createdAt

  def asDict(self):
    return




