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
    self.assertEqual(taskUnit.createdAt, self.createdAt)
    self.assertEqual(taskUnit.deadline, self.deadline)
    self.assertEqual(taskUnit.profit, self.profit)
    self.assertEqual(taskUnit.processing, self.processing)
    self.assertEqual(taskUnit.taskID, self.taskID)
    self.assertEqual(taskUnit.item, item)


  def test_asDict(self):
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID
    )
    expectedResult = {
      "id": self.taskID,
      "releaseISO": "",
      "deadlineISO": "",
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing
    }
    result = taskUnit.asDict()
    expectedResult["releaseISO"] = result["releaseISO"] # this is ok
    expectedResult["deadlineISO"] = result["deadlineISO"] # this is ok
    self.assertEqual(taskUnit.asDict(), expectedResult)

  def test_priority(self):
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID
    )
    from proactive.utils import timeutil
    # As expected priority is just the deadline of the task, calculate it.
    deadline = timeutil.addSeconds(self.createdAt, self.deadline)
    expectedPriority = deadline
    self.assertEqual(taskUnit.priority(), expectedPriority)
