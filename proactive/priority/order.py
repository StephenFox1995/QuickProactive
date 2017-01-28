class Order(object):
  class Status(object):
    UNPROCESSED = "unprocessed"
    PROCESSED = "processed"

  def __init__(self, orderID, status, processing, customerCoordinates, createdAt, cost):
    """
      @param orderID:(str) The id of the order.
      @param profit:(double) The profit from this order.
      @param customerCoordinates:(object) Contains coordinates such as {"lat": x, "lng": y}
    """
    self.orderID = orderID
    self.status = status
    self.processing = processing
    self.customerCoordinates = customerCoordinates
    self.cost = cost
    self.createdAt = createdAt

