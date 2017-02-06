from random import randint
from math import ceil
from unittest import TestCase
from datetime import datetime
from proactive.priority.taskmanager import TaskManager
from proactive.priority.taskunit import TaskUnit
from proactive.priority.exceptions import LateDeadlineException
from .testutil import tHour


class TestTaskManager(TestCase):

  def tPeriod(self):
    return (
      datetime(2017, 1, 1, 8, 0, 0, 0),
      datetime(2017, 1, 1, 21, 0, 0, 0)
    )


  def test_addTask(self):
    task = TaskUnit(
      createdAt=tHour(0, 0),
      deadline=tHour(10, 00),
      profit=0,
      processing=0,
      release=tHour(9, 30),
      taskID="t1"
    )
    taskManager = TaskManager(period=self.tPeriod())
    taskManager.addTask(task)
    self.assertEqual(taskManager.tasks[0], task)


  def test_numberOfConflicts(self):
    tasks = [
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
      )
    ]
    taskManager = TaskManager(period=self.tPeriod())
    taskManager.addTasks(tasks)
    conflicts = taskManager.findConflicts().allGreaterThan(2)
    self.assertEqual(len(conflicts), 1)


  def test_numberOfNonConflicts(self):
    tasks = [
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
        taskID="t6"
      )
    ]
    taskManager = TaskManager(period=self.tPeriod())
    taskManager.addTasks(tasks)
    nonConflicts = taskManager.findNonConflicts()
    self.assertEqual(len(nonConflicts), 2)

  def test_highestWorkersNeeded(self):
    tasks = [
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
        taskID="t6"
      )
    ]
    taskManager = TaskManager(period=self.tPeriod())
    taskManager.addTasks(tasks)
    workersNeeded = taskManager.highestNumberOfWorkersNeeded(multitask=2)
    self.assertEqual(workersNeeded, 2)


  def test_workersNeeded(self):
    taskManager = TaskManager(period=self.tPeriod())
    for _ in range(0, 1000): # try 100 difference numbers
      conflicts = randint(1, 100)
      multitask = randint(1, 5)
      expectedWorkers = ceil(float(conflicts)/float(multitask))
      actualWorkers = taskManager.workersNeeded(conflicts, multitask)
      self.assertEqual(actualWorkers, expectedWorkers)


  def test_taskAfterDeadline(self):
    task = TaskUnit(
      createdAt=tHour(0, 0),
      deadline=tHour(21, 1),
      profit=0,
      processing=0,
      release=tHour(16, 25),
      taskID="t1"
    )
    taskManager = TaskManager(period=self.tPeriod())
    with self.assertRaises(LateDeadlineException):
      taskManager.addTask(task)
