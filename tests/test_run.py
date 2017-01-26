from unittest2 import TestLoader, TextTestRunner, TestSuite
import test_order
from test_order import OrderTest
from test_orderpriority import OrderPriorityQueueTest

if __name__ == "__main__":
  loader = TestLoader()
  suite = TestSuite([
    loader.loadTestsFromTestCase(OrderTest),
    loader.loadTestsFromTestCase(OrderPriorityQueueTest)
  ])
  runner = TextTestRunner(verbosity=2)
  runner.run(suite)

