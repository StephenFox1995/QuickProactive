from unittest import TestCase
from proactive.priority.workerqueue import WorkerQueue
from proactive.priority.worker import Worker
from .testutil import tHour

class TestWorkerQueue(TestCase):
  def test_maxTasksAchievable(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    ]
    worker3 = Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    worker4 = Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    workerQ = WorkerQueue()
    workerQ.put(workers)
    self.assertEqual(workerQ.maxTasksAchievable(), 4)
    workerQ.put(worker3)
    self.assertEqual(workerQ.maxTasksAchievable(), 5)
    workerQ.put(worker4)
    self.assertEqual(workerQ.maxTasksAchievable(), 6)

  def test_removeWorker(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    workerQ = WorkerQueue()
    workerQ.put(workers)
    workerQ.removeWorker(workers[2])
    self.assertEqual(workerQ.nextWorker(), workers[0])
    self.assertEqual(workerQ.nextWorker(), workers[1])
    self.assertEqual(workerQ.nextWorker(), workers[3])
    self.assertEqual(workerQ.size(), 3)

  def test_putList(self):
    workers1 = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
    ]
    workers2 = [
      Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
    ]
    workerQ = WorkerQueue()
    workerQ.put(workers1)
    self.assertEqual(workerQ.nextWorker(), workers1[0])
    self.assertEqual(workerQ.nextWorker(), workers1[1])
    workerQ.put(workers2)
    self.assertEqual(workerQ.nextWorker(), workers1[0])
    self.assertEqual(workerQ.nextWorker(), workers1[1])
    self.assertEqual(workerQ.nextWorker(), workers2[0])
    self.assertEqual(workerQ.nextWorker(), workers2[1])

  def test_putWorkers(self):
    worker1 = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    worker2 = Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
    worker3 = Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
    worker4 = Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),

    workerQ = WorkerQueue()
    workerQ.put(worker1)
    self.assertEqual(workerQ.nextWorker(), worker1)
    workerQ.put(worker2)
    self.assertEqual(workerQ.nextWorker(), worker1)
    self.assertEqual(workerQ.nextWorker(), worker2)
    workerQ.put(worker3)
    self.assertEqual(workerQ.nextWorker(), worker1)
    self.assertEqual(workerQ.nextWorker(), worker2)
    self.assertEqual(workerQ.nextWorker(), worker3)
    workerQ.put(worker4)
    self.assertEqual(workerQ.nextWorker(), worker1)
    self.assertEqual(workerQ.nextWorker(), worker2)
    self.assertEqual(workerQ.nextWorker(), worker3)
    self.assertEqual(workerQ.nextWorker(), worker4)


  def test_availableWorkersInPeriod(self):
    worker1 = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    worker2 = Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)

    workerQ = WorkerQueue()
    workerQ.put(worker1)
    workerQ.put(worker2)
    availableWorkers = workerQ.availableWorkersDuringPeriod(tHour(00, 00), tHour(23, 59))
    self.assertEqual(availableWorkers[0], worker1)
    self.assertEqual(availableWorkers[1], worker2)
    self.assertEqual(len(availableWorkers), 2)
