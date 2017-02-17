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


  def _finishTask(self, taskID):
    for task in self._assignedTasks:
      if task.taskID == taskID:
        self._assignedTasks.remove(task)
    for task in self._unassignedTasks:
      if task.taskID == taskID:
        self._assignedTasks.remove(task)
    for worker in self._workers: # ask whatever worker has the task to unassign it.
      try:
        worker.unassignTask(task)
        break
      except UnkownTaskException:
        pass
    try:
      task = self._taskSet.remove(taskID)
    except UnkownTaskException:
      pass


  def _workersAvailableInPeriod(self, begin, end):
    availableWorkers = []
    for worker in self._workers:
      if worker.availableInPeriod(begin, end):
        availableWorkers.append(worker)
    return availableWorkers


  def workersNeededForConflicts(self):
    conflicts = self._taskSet.findConflicts().all()
    dataset = {
      "conflicts": []
    }
    for conflict in conflicts:
      workersNeeded = self.workersNeeded(len(conflict), 2)
      data = {
        "workersNeeded": workersNeeded,
        "begin": conflict.period.begin.isoformat(),
        "end": conflict.period.end.isoformat()
        }
      dataset["conflicts"].append(data)
    return dataset


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
        # check if this task was ever in unassigned tasks because
        # at some stage it could not be assigned.
        # if so take it out of unassigned and put in assigned list.
        if task in self._unassignedTasks:
          self._unassignedTasks.remove(task)
          self._assignedTasks.append(task)
        else: # not in unassigned before so put straight into assigned.
          self._assignedTasks.append(task)
        return # task has been assigned return from method
      else:
        continue
    # task was not assigned.
    raise UnassignableTaskException
