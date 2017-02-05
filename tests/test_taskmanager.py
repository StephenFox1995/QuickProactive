from random import randint
from math import ceil
from unittest import TestCase
from datetime import datetime
from proactive.priority.taskmanager import TaskManager
from proactive.priority.taskunit import TaskUnit

class TestTaskManager(TestCase):

  def tHour(self, hour, minute):
    return datetime(2017, 1, 1, hour, minute, 0, 0)

  def test_numberOfConflicts(self):
    tasks = [
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(10, 00),
        profit=0,
        processing=1800,
        release=self.tHour(9, 30),
        taskID="t1"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(11, 00),
        profit=0,
        processing=0,
        release=self.tHour(9, 40),
        taskID="t2"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 30),
        taskID="t3"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 35),
        taskID="t4"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 30),
        profit=0,
        release=self.tHour(11, 50),
        processing=0,
        taskID="t5"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(15, 30),
        profit=0,
        processing=0,
        release=self.tHour(14, 50),
        taskID="t6"
      )
    ]
    taskManager = TaskManager(period=(8, 9))
    taskManager.addTasks(tasks)
    conflicts = taskManager.findConflicts().allGreaterThan(2)
    self.assertEqual(len(conflicts), 1)


  def test_numberOfNonConflicts(self):
    tasks = [
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(10, 00),
        profit=0,
        processing=0,
        release=self.tHour(9, 30),
        taskID="t1"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(11, 00),
        profit=0,
        processing=0,
        release=self.tHour(9, 40),
        taskID="t2"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 30),
        taskID="t3"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 35),
        taskID="t4"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 30),
        profit=0,
        release=self.tHour(11, 50),
        processing=0,
        taskID="t5"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(15, 30),
        profit=0,
        processing=0,
        release=self.tHour(14, 50),
        taskID="t6"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(16, 30),
        profit=0,
        processing=0,
        release=self.tHour(16, 25),
        taskID="t6"
      )
    ]
    taskManager = TaskManager(period=(8, 9))
    taskManager.addTasks(tasks)
    nonConflicts = taskManager.findNonConflicts()
    self.assertEqual(len(nonConflicts), 2)

  def test_highestWorkersNeeded(self):
    tasks = [
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(10, 00),
        profit=0,
        processing=0,
        release=self.tHour(9, 30),
        taskID="t1"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(11, 00),
        profit=0,
        processing=0,
        release=self.tHour(9, 40),
        taskID="t2"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 30),
        taskID="t3"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 00),
        profit=0,
        processing=0,
        release=self.tHour(11, 35),
        taskID="t4"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(12, 30),
        profit=0,
        release=self.tHour(11, 50),
        processing=0,
        taskID="t5"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(15, 30),
        profit=0,
        processing=0,
        release=self.tHour(14, 50),
        taskID="t6"
      ),
      TaskUnit(
        createdAt=self.tHour(0, 0),
        deadline=self.tHour(16, 30),
        profit=0,
        processing=0,
        release=self.tHour(16, 25),
        taskID="t6"
      )
    ]
    taskManager = TaskManager(period=(8, 9))
    taskManager.addTasks(tasks)
    workersNeeded = taskManager.highestNumberOfWorkersNeeded(multitask=2)
    self.assertEqual(workersNeeded, 2)


  def test_workersNeeded(self):
    taskManager = TaskManager(period=(8, 9))
    for _ in range(0, 1000): # try 100 difference numbers
      conflicts = randint(1, 100)
      multitask = randint(1, 5)
      expectedWorkers = ceil(float(conflicts)/float(multitask))
      actualWorkers = taskManager.workersNeeded(conflicts, multitask)
      self.assertEqual(actualWorkers, expectedWorkers)
