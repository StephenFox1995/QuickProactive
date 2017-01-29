from unittest2 import TestLoader, TextTestRunner, TestSuite
from .test_taskunitpriorityqueue import TestTaskUnitPriorityQueue
from .test_taskunit import TestTaskUnit
from .test_order import TestOrder
from .test_release import TestRelease
from .test_timeutil import TestTimeutil

if __name__ == "__main__":
  loader = TestLoader()
  suite = TestSuite([
    loader.loadTestsFromTestCase(TestRelease),
    loader.loadTestsFromTestCase(TestTaskUnitPriorityQueue),
    loader.loadTestsFromTestCase(TestOrder),
    loader.loadTestsFromTestCase(TestTaskUnit),
    loader.loadTestsFromTestCase(TestTimeutil)
  ])
  runner = TextTestRunner(verbosity=2)
  runner.run(suite)

