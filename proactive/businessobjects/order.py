from .dataitem import DataItem

class Order(DataItem):
  class Status(object):
    UNPROCESSED = "unprocessed"
    PROCESSED = "processed"

  def __init__(self, orderID, status, processing, customerCoordinates, travelMode, createdAt, cost, products):
    self._orderID = orderID
    self._status = status
    self._processing = processing
    self._customerCoordinates = customerCoordinates
    self._travelMode = travelMode
    self._cost = cost
    self._createdAt = createdAt
    self._products = products


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
  def travelMode(self):
    return self._travelMode

  @property
  def cost(self):
    return self._cost

  @property
  def createdAt(self):
    return self._createdAt

  @property
  def products(self):
    return self._products

  def asDict(self):
    return self.products




