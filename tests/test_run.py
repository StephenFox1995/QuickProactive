from unittest2 import TestLoader, TextTestRunner, TestSuite
from .test_taskunitpriorityqueue import TestTaskUnitPriorityQueue
from .test_release import TestRelease

if __name__ == "__main__":
  loader = TestLoader()
  suite = TestSuite([
    loader.loadTestsFromTestCase(TestRelease),
    loader.loadTestsFromTestCase(TestTaskUnitPriorityQueue)
  ])
  runner = TextTestRunner(verbosity=2)
  runner.run(suite)

