from unittest import TestCase
from proactive.priority.taskset import TaskSet
from proactive.priority.taskunit import TaskUnit
from proactive.priority.period import Period
from .testutil import tHour

class TestTaskSet(TestCase):
  def setUp(self):
    """
      Visually the tasks would look something like this:

                t1 ----
                  t2 -----------------------
                                                          t3 -----
                                                            t4 ----
                                                              t5 ---------------
                                                                                                                              t6 --------------                     t7-
      9.00-----9.30-----|10.00-----10.30-----|11.00-----11.30-----|12.00-----12.30-----|13.00-----13.30-----|14.00-----14.30-----|15.00-----15.30-----|16.00-----16.30
    """
    self.tasks = [
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(10, 00),
        profit=0,
        processing=0,
        release=tHour(9, 30),
        taskID="t1"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(11, 00),
        profit=0,
        processing=0,
        release=tHour(9, 40),
        taskID="t2"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(12, 00),
        profit=0,
        processing=0,
        release=tHour(11, 30),
        taskID="t3"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(12, 00),
        profit=0,
        processing=0,
        release=tHour(11, 35),
        taskID="t4"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(12, 30),
        profit=0,
        release=tHour(11, 50),
        processing=0,
        taskID="t5"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(15, 30),
        profit=0,
        processing=0,
        release=tHour(14, 50),
        taskID="t6"
      ),
      TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(16, 30),
        profit=0,
        processing=0,
        release=tHour(16, 25),
        taskID="t7"
      )
    ]


  def _taskSet(self):
    taskSet = TaskSet()
    taskSet.add(self.tasks[0])
    taskSet.add(self.tasks[1])
    taskSet.add(self.tasks[2])
    taskSet.add(self.tasks[3])
    taskSet.add(self.tasks[4])
    taskSet.add(self.tasks[5])
    taskSet.add(self.tasks[6])
    return taskSet

  def test_add(self):
    taskSet = self._taskSet()
    self.assertEqual(len(taskSet.tasks), 7)

  def test_remove(self):
    taskSet = self._taskSet()
    taskSet.remove(self.tasks[0])
    self.assertEqual(len(taskSet.tasks), 6)

  def test_conflicts(self):
    taskSet = self._taskSet()
    self.assertEqual(len(taskSet.findConflicts().all()), 2)

  def test_conflictPeriod(self):
    taskSet = self._taskSet()
    conflictSet = taskSet.findConflicts().all()
    expectedConflictPeriod1 = Period(tHour(9, 30), tHour(11, 00))
    expectedConflictPeriod2 = Period(tHour(11, 30), tHour(12, 30))
    conflict1 = conflictSet[0]
    conflict2 = conflictSet[1]
    self.assertEqual(expectedConflictPeriod1.begin, conflict1.period.begin)
    self.assertEqual(expectedConflictPeriod1.end, conflict1.period.end)
    self.assertEqual(expectedConflictPeriod2.begin, conflict2.period.begin)
    self.assertEqual(expectedConflictPeriod2.end, conflict2.period.end)
