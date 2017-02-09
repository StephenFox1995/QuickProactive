from unittest import TestCase
from datetime import datetime
from proactive.priority.worker import Worker
from proactive.priority.taskunit import TaskUnit
from proactive.priority.exceptions import MaxTaskLimitReached


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
    worker = Worker("W1", 2)
    worker.assignTask(self.task1)
    worker.assignTask(self.task2)
    with self.assertRaises(MaxTaskLimitReached):
      worker.assignTask(self.task3)


  def test_exactTaskLimit(self):
    worker = Worker("W1", 2)
    worker.assignTask(self.task1)
    worker.assignTask(self.task2)
    self.assertEqual(len(worker.assignedTasks), 2)

  def test_canAssignTasks(self):
    worker = Worker("W1", 2)
    self.assertTrue(worker.canAssignTask())
    worker.assignTask(self.task1)
    self.assertTrue(worker.canAssignTask())
    worker.assignTask(self.task2)
    self.assertFalse(worker.canAssignTask())
