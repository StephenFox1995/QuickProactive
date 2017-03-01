from unittest import TestCase
from proactive.priority.taskset import TaskSet
from proactive.priority.period import Period
from .test_tasksets import testtaskset
from .testutil import tHour

class TestTaskSet(TestCase):
  def setUp(self):
    self.tasks = testtaskset


  def _taskSet(self):
    taskSet = TaskSet()
    taskSet.add(self.tasks[0])
    taskSet.add(self.tasks[1])
    taskSet.add(self.tasks[2])
    taskSet.add(self.tasks[3])
    taskSet.add(self.tasks[4])
    taskSet.add(self.tasks[5])
    taskSet.add(self.tasks[6])
    taskSet.add(self.tasks[7])
    taskSet.add(self.tasks[8])
    return taskSet


  def test_add(self):
    taskSet = self._taskSet()
    self.assertEqual(len(taskSet.tasks), 9)

  def test_remove(self):
    taskSet = self._taskSet()
    taskSet.remove(self.tasks[0])
    self.assertEqual(len(taskSet.tasks), 8)

  def test_conflicts(self):
    taskSet = self._taskSet()
    conflicts, nonConflicts = taskSet.findConflicts()
    self.assertEqual(len(conflicts.all()), 2)
    self.assertEqual(len(nonConflicts.all()), 1)

  def test_conflictPeriod(self):
    taskSet = self._taskSet()
    conflictSet = taskSet.findConflicts()[0].all()
    expectedConflictPeriod1 = Period(tHour(9, 30), tHour(11, 00))
    expectedConflictPeriod2 = Period(tHour(11, 30), tHour(13, 30))
    conflict1 = conflictSet[0]
    conflict2 = conflictSet[1]
    self.assertEqual(expectedConflictPeriod1.begin, conflict1.period.begin)
    self.assertEqual(expectedConflictPeriod1.end, conflict1.period.end)
    self.assertEqual(expectedConflictPeriod2.begin, conflict2.period.begin)
    self.assertEqual(expectedConflictPeriod2.end, conflict2.period.end)
