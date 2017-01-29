from datetime import datetime
from proactive.priority.taskunit import TaskUnit
from unittest2 import TestCase


class TestTaskUnit(TestCase):
  def setUp(self):
    self.createdAt = datetime.now()
    self.taskID = "test1234"
    self.deadline = 500
    self.profit = 2.56
    self.processing = 100


  def test_init(self):
    item = [1, 2, 3, 4]
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID,
      item=item
    )
    self.assertEquals(taskUnit.createdAt, self.createdAt)
    self.assertEquals(taskUnit.deadline, self.deadline)
    self.assertEquals(taskUnit.profit, self.profit)
    self.assertEquals(taskUnit.processing, self.processing)
    self.assertEquals(taskUnit.taskID, self.taskID)
    self.assertEqual(taskUnit.item, item)

