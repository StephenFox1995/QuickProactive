from random import randint
from math import ceil
from unittest import TestCase
from datetime import datetime
from mock import patch
from proactive.priority.taskmanager import TaskManager
from proactive.priority.taskunit import TaskUnit
from proactive.priority.exceptions import (
  LateDeadlineException,
  UnfinishedTasksHeldByWorkerException,
  UnkownWorkerException)
from proactive.priority.worker import Worker
from .test_tasksets import testtaskset
from .testutil import tHour


class TestTaskManager(TestCase):
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
    self.tasks = testtaskset

  def tPeriod(self):
    return (
      datetime(2017, 1, 1, 8, 0, 0, 0),
      datetime(2017, 1, 1, 21, 0, 0, 0)
    )

  def test_addTask(self):
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addTask(self.tasks[0])
    self.assertEqual(taskManager.taskSet.tasks[0], self.tasks[0])

  def test_finishTasks(self):
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addTask(self.tasks[0])
    taskManager.addTask(self.tasks[1])
    self.assertEqual(len(taskManager.taskSet.tasks), 2)
    taskManager.finishTask(self.tasks[0].taskID)
    self.assertEqual(len(taskManager.taskSet.tasks), 1)
    taskManager.finishTask(self.tasks[1].taskID)
    self.assertEqual(len(taskManager.taskSet.tasks), 0)

  def test_workersNeeded(self):
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    for _ in range(0, 1000): # try 1000 different numbers
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
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    with self.assertRaises(LateDeadlineException):
      taskManager.addTask(task)

  def test_addWorkers(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addWorkers(workers)
    self.assertEqual(len(taskManager.workers), 2)

  def test_removeWorker(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addWorkers(workers)
    taskManager.removeWorker(workers[0].workerID)
    self.assertEqual(len(taskManager.workers), 1)

  def test_removeWorkerAfterAssigningTasks(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addTasks([self.tasks[0], self.tasks[1]])
    taskManager.addWorkers(workers)
    taskManager.assignTasksToWorkers()
    # make sure the exception is thrown as the tasks are not finished yet.
    with self.assertRaises(UnfinishedTasksHeldByWorkerException):
      taskManager.removeWorker(workers[0].workerID)
    # finish the tasks and remove workers
    taskManager.finishTask(self.tasks[0].taskID)
    taskManager.removeWorker(workers[0].workerID)
    self.assertEqual(len(taskManager.workers), 1)
    taskManager.finishTask(self.tasks[1].taskID)
    taskManager.removeWorker(workers[1].workerID)
    self.assertEqual(len(taskManager.workers), 0)

  def test_removeUnkownWorker(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addWorker(worker)
    with self.assertRaises(UnkownWorkerException):
      taskManager.removeWorker("thisworkerdoesnotexists")

  def test_addWorker(self):
    worker = Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addWorker(worker)
    self.assertEqual(len(taskManager.workers), 1)

  def test_addWorkersAfterInitialAssignment(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addTasks(self.tasks)
    taskManager.addWorkers(workers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(self.tasks[0], workers[0].assignedTasks[0])
    self.assertEqual(self.tasks[1], workers[1].assignedTasks[0])

  def test_assignTasksToWorkers(self):
    initialWorkers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    extraWorkers = [
      Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(self.tPeriod(), multitask=1)
    taskManager.addTasks(self.tasks)
    taskManager.addWorkers(initialWorkers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(self.tasks[0], initialWorkers[0].assignedTasks[0]) #check w1
    self.assertEqual(self.tasks[1], initialWorkers[1].assignedTasks[0]) #check w2
    self.assertEqual(self.tasks[2], initialWorkers[2].assignedTasks[0]) #check w3
    self.assertEqual(taskManager.unassignedTasks[0], self.tasks[3])
    self.assertEqual(taskManager.unassignedTasks[1], self.tasks[4])
    self.assertEqual(taskManager.unassignedTasks[2], self.tasks[5])
    #add more tasks and make sure they were assigned to the new workers.
    taskManager.addWorkers(extraWorkers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(self.tasks[3], extraWorkers[0].assignedTasks[0]) #check w4
    self.assertEqual(self.tasks[4], extraWorkers[1].assignedTasks[0]) #check w5
    self.assertEqual(taskManager.unassignedTasks[0], self.tasks[5])

  @patch('proactive.priority.taskunit.TaskUnit.isProcessing')
  def test_assignTaskToWorkersThatNeedsToBeSwapped(self, isProcessing):
    # mock task unit so its isProcessing method always returns true
    # as it is time dependent, and will fail if this test if run at certain times
    isProcessing.return_value = False

    task1 = TaskUnit(
        createdAt=tHour(0, 0),
        deadline=tHour(10, 00),
        profit=0,
        processing=0,
        release=tHour(9, 30),
        taskID="t1"
      )
    task2 = TaskUnit(
      createdAt=tHour(0, 0),
      deadline=tHour(11, 00),
      profit=0,
      processing=0,
      release=tHour(9, 40),
      taskID="t2"
    )
    task3 = TaskUnit(
      createdAt=tHour(0, 0),
      deadline=tHour(12, 00),
      profit=0,
      processing=0,
      release=tHour(11, 30),
      taskID="t3"
    )
    workers = [
      Worker(workerID="W4", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addTask(task2)
    taskManager.addTask(task3)
    taskManager.addWorkers(workers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(task2, workers[0].assignedTasks[0])
    self.assertEqual(task3, workers[1].assignedTasks[0])
    taskManager.addTask(task1) # earlier release, therfore should be swapped.
    taskManager.assignTasksToWorkers()
    self.assertEqual(task1, workers[0].assignedTasks[0]) # should be assigned to worker
    self.assertIsNone(task3.assignedWorker) # workers for task3 should be None


  def test_assignedTasksCountAndUnassignedTasksCount(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addTask(self.tasks[0])
    taskManager.addTask(self.tasks[1])
    taskManager.addTask(self.tasks[2])
    taskManager.addWorkers(workers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(len(taskManager.assignedTasks), 2)
    self.assertEqual(len(taskManager.unassignedTasks), 1)

  def test_finishTasksAfterAssigningTasksToWorkers(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W3", begin=tHour(0, 00), end=tHour(23, 59), multitask=1)
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addTask(self.tasks[0])
    taskManager.addTask(self.tasks[1])
    taskManager.addWorkers(workers)
    taskManager.assignTasksToWorkers()
    self.assertEqual(len(taskManager.workers), 3)
    taskManager.finishTask(self.tasks[0].taskID)
    self.assertEqual(len(workers[0].assignedTasks), 0)
    self.assertEqual(len(taskManager.workers), 3)

    taskManager.finishTask(self.tasks[1].taskID) # test with id too.
    self.assertEqual(len(workers[1].assignedTasks), 0)
    self.assertEqual(len(taskManager.workers), 3)

  def test_workerGetsAssignedAnotherTaskAfterFinishing(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addWorkers(workers)
    taskManager.addTasks(self.tasks)
    taskManager.assignTasksToWorkers()
    self.assertEqual(len(workers[0].assignedTasks), 1)
    self.assertEqual(len(workers[1].assignedTasks), 1)
    # check that task was unnasigned from worker.
    assignedTask = workers[0].assignedTasks[0]
    taskManager.finishTask(assignedTask.taskID)
    self.assertEqual(len(workers[0].assignedTasks), 0)
    # now assign tasks if theres any more.
    taskManager.assignTasksToWorkers()
    self.assertEqual(len(workers[0].assignedTasks), 1)

  def test_noConflictsAfterAllTasksRemoved(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=1),
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=1)
    taskManager.addWorkers(workers)
    taskManager.addTask(self.tasks[0])
    taskManager.addTask(self.tasks[1])
    taskManager.assignTasksToWorkers()
    conflicts = taskManager.analyseWorkersForNeededTaskSet()[0]
    self.assertEqual(conflicts[0].workersNeeded, 2)
    taskManager.finishTask(self.tasks[0].taskID)
    taskManager.finishTask(self.tasks[1].taskID)
    conflicts = taskManager.analyseWorkersForNeededTaskSet()[0]
    self.assertEqual(len(conflicts), 0) # there should be not conflicts

  def test_analyseWorkersNeededTaskSet(self):
    workers = [
      Worker(workerID="W1", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
      Worker(workerID="W2", begin=tHour(0, 00), end=tHour(23, 59), multitask=2),
    ]
    taskManager = TaskManager(period=self.tPeriod(), multitask=2)
    taskManager.addWorkers(workers)
    taskManager.addTasks(self.tasks)
    taskManager.assignTasksToWorkers()
    conflicts, nonConflicts = taskManager.analyseWorkersForNeededTaskSet()
    self.assertEqual(len(conflicts), 2)
    self.assertEqual(len(nonConflicts), 1)
