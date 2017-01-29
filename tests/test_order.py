from proactive.priority.order import Order
from unittest2 import TestCase
from datetime import datetime

class TestOrder(TestCase):
  def setUp(self):
    self.orderID = "test1234"
    self.status = Order.Status.UNPROCESSED
    self.processing = 100
    self.customerCoordinates = {"lat": 53.345466, "lng": -6.278987}
    self.cost = 2.56
    self.createdAt = datetime.now()


  def test_init(self):
    order = Order(
      orderID=self.orderID,
      status=self.status,
      processing=self.processing,
      customerCoordinates=self.customerCoordinates,
      cost=self.cost,
      createdAt=self.createdAt
    )
    self.assertEquals(order.orderID, self.orderID)
    self.assertEquals(order.status, self.status)
    self.assertEquals(order.processing, self.processing)
    self.assertEquals(order.customerCoordinates, self.customerCoordinates)
    self.assertEquals(order.cost, self.cost)
    self.assertEquals(order.createdAt, self.createdAt)

