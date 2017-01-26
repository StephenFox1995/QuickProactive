from proactive.priority.orderpriority import OrderPriorityQueue
from proactive.priority.order import Order
import unittest2

class OrderPriorityQueueTest(unittest2.TestCase):

  def test_count(self):
    items = [Order(1, 0, 300, 0)]
    pQueue = OrderPriorityQueue()
    pQueue.add(items)
    self.assertEqual(pQueue.count(), 1)

  def test_addToEmptyQueue(self):
    items = [Order(1, 0, 300, 0)]
    pQueue = OrderPriorityQueue()
    pQueue.add(items)
    self.assertEqual(pQueue.count(), 1)

  def test_addToPopulatedQueue(self):
    items = [
      Order(1, 0, 300, 0),
      Order(2, 0, 400, 0)
    ]
    pQueue = OrderPriorityQueue(items)
    item = Order(3, 0, 300, 0)
    pQueue.add(item)
    self.assertEqual(pQueue.count(), 3)

  def test_addWithNonListObject(self):
    item = Order(1, 0, 300, 0)
    pQueue = OrderPriorityQueue()
    pQueue.add(item)
    self.assertEqual(pQueue.count(), 1)

  def test_popEmptyQueue(self):
    pQueue = OrderPriorityQueue()
    with self.assertRaises(IndexError):
      pQueue.pop()

  def test_popPopulatedQueueFromConstructor(self):
    items = [
      Order(2, 300, 10, 0),
      Order(1, 100, 10, 0),
      Order(2, 200, 10, 0)
    ]
    pQueue = OrderPriorityQueue(items)
    """
      Items in the queue should be ordered :
      [
        Order(1, 100, 10, 0),
        Order(2, 200, 10, 0),
        Order(2, 300, 10, 0)
      ]
      As Order(1, 100, 10, 0) has the earliest deadline.
    """
    self.assertEqual(items[1], pQueue.pop())
    self.assertEqual(items[2], pQueue.pop())
    self.assertEqual(items[0], pQueue.pop())

  def test_popPopulatedQueueAfterAdd(self):
    items = [
      Order(2, 300, 10, 0),
      Order(1, 100, 10, 0),
      Order(2, 200, 10, 0)
    ]
    pQueue = OrderPriorityQueue()
    pQueue.add(items)
    self.assertEqual(items[1], pQueue.pop())
    self.assertEqual(items[2], pQueue.pop())
    self.assertEqual(items[0], pQueue.pop())

