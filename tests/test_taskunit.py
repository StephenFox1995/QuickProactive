from datetime import datetime
from unittest import TestCase
from proactive.priority.taskunit import TaskUnit
from proactive.utils import timeutil
from proactive.priority import release
from .testutil import tHour

class TestTaskUnit(TestCase):
  def setUp(self):
    self.createdAt = datetime.now()
    self.taskID = "test1234"
    self.deadline = 500
    self.profit = 2.56
    self.processing = 100
    self.globalTask = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing
    )


  def test_init(self):
    data = [1, 2, 3, 4]
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID,
      data=data
    )
    expectedRelease = release.releaseAt(self.deadline, self.processing, self.createdAt)
    self.assertEqual(taskUnit.createdAt, self.createdAt)
    self.assertEqual(taskUnit.deadline, self.deadline)
    self.assertEqual(taskUnit.profit, self.profit)
    self.assertEqual(taskUnit.processing, self.processing)
    self.assertEqual(taskUnit.taskID, self.taskID)
    self.assertEqual(taskUnit.data, data)
    self.assertEqual(taskUnit.release, expectedRelease)


  def test_asDict(self):
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID
    )
    # Calculate the correct ISO for task.
    expectedReleaseISO = release.releaseAt(
      self.deadline,
      self.processing,
      self.createdAt
    ).isoformat()
    expectedDeadlineISO = timeutil.addSeconds(self.createdAt, self.deadline).isoformat()
    expectedCreatedAtISO = self.createdAt.isoformat()

    expectedResult = {
      "id": self.taskID,
      "releaseISO": expectedReleaseISO,
      "deadlineISO": expectedDeadlineISO,
      "createdAtISO": expectedCreatedAtISO,
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing,
    }
    self.assertEqual(taskUnit.asDict(), expectedResult)

  def test_priority(self):
    taskUnit = TaskUnit(
      createdAt=self.createdAt,
      deadline=self.deadline,
      profit=self.profit,
      processing=self.processing,
      taskID=self.taskID
    )
    # As expected priority is just the release of the task, calculate it.
    expectedRelease = release.releaseAt(self.deadline, self.processing, self.createdAt)
    expectedPriority = expectedRelease
    self.assertEqual(taskUnit.priority(), expectedPriority)

  def test_laterReleaseThanDeadline(self):
    with self.assertRaises(ValueError):
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(12, 30),
        profit=self.profit,
        processing=self.processing,
        release=tHour(13, 30),
        taskID=self.taskID
      )
