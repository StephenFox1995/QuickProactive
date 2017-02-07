from unittest import TestLoader, TextTestRunner, TestSuite
from .test_taskunitpriorityqueue import TestTaskUnitPriorityQueue
from .test_taskunit import TestTaskUnit
from .test_order import TestOrder
from .test_release import TestRelease
from .test_timeutil import TestTimeutil
from .test_travel import TestTravel
from .test_taskmanager import TestTaskManager
from .test_business import TestPeriod

if __name__ == "__main__":
  loader = TestLoader()
  suite = TestSuite([
    loader.loadTestsFromTestCase(TestRelease),
    loader.loadTestsFromTestCase(TestTaskUnitPriorityQueue),
    loader.loadTestsFromTestCase(TestOrder),
    loader.loadTestsFromTestCase(TestTaskUnit),
    loader.loadTestsFromTestCase(TestTimeutil),
    loader.loadTestsFromTestCase(TestTravel),
    loader.loadTestsFromTestCase(TestTaskManager),
    loader.loadTestsFromTestCase(TestPeriod)
  ])
  runner = TextTestRunner(verbosity=2)
  runner.run(suite)

