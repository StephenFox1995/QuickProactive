from datetime import datetime
import weakref
from .exceptions import (
  LateDeadlineException,
  UnassignableTaskException,
  UnkownTaskException,
  DuplicateTaskException)
from .workerqueue import WorkerQueue
from .worker import Worker
from .taskset import TaskSet
from .conflict import Conflict

class TaskManager(object):
  def __init__(self, period):
    self._taskSet = TaskSet()
    self._workersQ = WorkerQueue()
    self._workers = []
    self._assignedTasks = []
    self._unassignedTasks = []
    if isinstance(period[0], datetime) and isinstance(period[1], datetime):
      self._start = period[0]
      self._end = period[1]
    else:
      raise TypeError(
        "period[0] and period[1] should be %s" % datetime
      )


  @property
  def assignedTasks(self):
    return self._assignedTasks


  @property
  def unassignedTasks(self):
    return self._unassignedTasks


  @property
  def taskSet(self):
    """
      Returns all the tasks the manager currently holds.
      The tasks are return in no particular order.
    """
    return self._taskSet


  @property
  def workers(self):
    return self._workers


  def addTask(self, task):
    if task.deadline > self._end:
      raise LateDeadlineException(
        "Cannot process this task as it's deadline is %s is after %s"
        % (task.deadline, self._end)
      )
    try:
      self._taskSet.add(task)
      self._unassignedTasks.append(task)
    except DuplicateTaskException:
      pass


  def addTasks(self, tasks):
    for task in tasks:
      self.addTask(task)


  def finishTask(self, taskID):
    """
      When a task if finished, call this method.
    """
    self._finishTask(taskID)


  def _getTask(self, taskID):
    """
      Finds a task by id in assigned or unassigned task lists.
    """
    for task in self._assignedTasks:
      if task.taskID == taskID:
        return task
    for task in self._unassignedTasks:
      if task.taskID == taskID:
        return task


  def _finishTask(self, taskID):
    task = self._getTask(taskID)
    if task in self._assignedTasks:
      self._assignedTasks.remove(task)
    if task in self._unassignedTasks:
      self._unassignedTasks.remove(task)
    for worker in self._workers: # ask whatever worker has the task to unassign it.
      try:
        worker.unassignTask(taskID)
        break
      except UnkownTaskException:
        pass
    try:
      task = self._taskSet.remove(task)
    except UnkownTaskException:
      pass


  def _workersAvailableInPeriod(self, begin, end):
    availableWorkers = []
    for worker in self._workers:
      if worker.availableInPeriod(begin, end):
        availableWorkers.append(worker)
    return availableWorkers


  def analyseWorkersForNeededTaskSet(self, multitask=2):
    """
      Analyses all the conflicts and non conflicts within the task set.
      Set the appropriate properties for each conflict.
    """
    conflicts = self._taskSet.findConflicts()[0].all()
    nonConflicts = self._taskSet.findConflicts()[1].all()
    for conflict in conflicts:
      begin = conflict.period.begin
      end = conflict.period.end
      workersNeeded = self.workersNeeded(len(conflict), multitask)
      workersAvailable = len(self._workersQ.availableWorkersDuringPeriod(begin, end))
      conflict.workersNeeded = int(workersNeeded)
      conflict.availableWorkers = workersAvailable
    for nonConflict in nonConflicts:
      begin = nonConflict.period.begin
      end = nonConflict.period.end
      workersAvailable = len(self._workersQ.availableWorkersDuringPeriod(begin, end))
      nonConflict.workersNeeded = 1
      nonConflict.availableWorkers = workersAvailable
    return conflicts, nonConflicts


  def workersNeeded(self, k, m):
    """
      Calculates the number of employees needed to deal with a conflict.
      @param k:() The number of conflicts
      @param m:() The highest number of tasks employees can service simultaneously.
    """
    # formula: k/m
    from math import ceil
    return ceil(float(k)/float(m))


  def addWorker(self, worker):
    if isinstance(worker, Worker):
      self._workersQ.put(worker)
      self._workers.append(worker)
    else:
      raise TypeError(
        "Cannot add worker type %s, should be %s" % Worker
      )


  def addWorkers(self, workers):
    for w in workers:
      self.addWorker(w)


  def assignTasksToWorkers(self):
    tasksToPutIntoSet = []
    for task in self._taskSet:
      try:
        self._assignTaskToAnyWorkerOrFail(task)
      except UnassignableTaskException:
        tasksToPutIntoSet.append(task)
        if task not in self._unassignedTasks:
          self._unassignedTasks.append(task)
    for task in tasksToPutIntoSet: # put all unassigned tasks back into set.
      self._taskSet.add(task)


  def _assignTaskToAnyWorkerOrFail(self, task):
    maxTasksAchievable = self._workersQ.maxTasksAchievable()
    for _ in range(0, maxTasksAchievable):
      # get next worker
      worker = self._workersQ.nextWorker()
      # check if we've already tried to assign it  task.
      if worker.canAssignTask():
        worker.assignTask(task)
        task.assignWorker(weakref.ref(worker)())
        if task in self._unassignedTasks:
          self._unassignedTasks.remove(task)
          self._assignedTasks.append(task)
        else:
          self._assignedTasks.append(task)
        return # task has been assigned return from method
      else:
        continue
    # task was not assigned.
    raise UnassignableTaskException
