from unittest import TestCase
from proactive.priority.workerqueue import WorkerQueue
from proactive.priority.worker import Worker

class TestWorkerQueue(TestCase):
  def test_maxTasksAchievable(self):
    workers = [
      Worker("W1", 2),
      Worker("W2", 2)
    ]
    worker3 = Worker("W3", 1)
    worker4 = Worker("W4", 1)
    workerQ = WorkerQueue()
    workerQ.put(workers)
    self.assertEqual(workerQ.maxTasksAchievable(), 4)
    workerQ.put(worker3)
    self.assertEqual(workerQ.maxTasksAchievable(), 5)
    workerQ.put(worker4)
    self.assertEqual(workerQ.maxTasksAchievable(), 6)

  def test_putList(self):
    workers1 = [Worker("W1", 2), Worker("W2", 2)]
    workers2 = [Worker("W3", 1), Worker("W4", 1)]
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
    worker1 = Worker("W1", 2)
    worker2 = Worker("W2", 2)
    worker3 = Worker("W3", 1)
    worker4 = Worker("W4", 1)

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
