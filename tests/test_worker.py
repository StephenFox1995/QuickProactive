from unittest import TestCase
from datetime import datetime
from proactive.priority.worker import Worker
from proactive.priority.taskunit import TaskUnit
from proactive.priority.exceptions import MaxTaskLimitReachedException
from .testutil import tHour

class TestWorker(TestCase):
  def setUp(self):
    self.task1 = TaskUnit(
      createdAt=datetime.now(),
      deadline=500,
      profit=2.56,
      processing=100,
      taskID="test1234"
    )
    self.task2 = TaskUnit(
      createdAt=datetime.now(),
      deadline=500,
      profit=2.56,
      processing=100,
      taskID="test1234"
    )
    self.task3 = TaskUnit(
      createdAt=datetime.now(),
      deadline=500,
      profit=2.56,
      processing=100,
      taskID="test1234"
    )

  def test_maxTasksLimit(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    worker.assignTask(self.task1)
    worker.assignTask(self.task2)
    with self.assertRaises(MaxTaskLimitReachedException):
      worker.assignTask(self.task3)

  def test_exactTaskLimit(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    worker.assignTask(self.task1)
    worker.assignTask(self.task2)
    self.assertEqual(len(worker.assignedTasks), 2)

  def test_canAssignTasks(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    self.assertFalse(worker.hasReachedTaskLimit())
    worker.assignTask(self.task1)
    self.assertFalse(worker.hasReachedTaskLimit())
    worker.assignTask(self.task2)
    self.assertTrue(worker.hasReachedTaskLimit())

  def test_unnasignTask(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    worker.assignTask(self.task1)
    worker.unassignTask(self.task1.taskID)
    self.assertEqual(len(worker.assignedTasks), 0)

  def test_availableInPeriod(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2)
    available = worker.availableInPeriod(begin=tHour(12, 00), end=tHour(13, 00))
    self.assertTrue(available)
