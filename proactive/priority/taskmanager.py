from datetime import datetime
import weakref
from .exceptions import (
  LateDeadlineException,
  UnassignableTaskException,
  UnkownTaskException,
  DuplicateTaskException,
  UnfinishedTasksHeldByWorkerException,
  UnkownWorkerException)
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
    conflicts, nonConflicts = self._taskSet.findConflicts()
    conflicts = conflicts.all()
    nonConflicts = nonConflicts.all()
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
        "Cannot add worker %s, should be %s" % (type(worker), Worker)
      )


  def addWorkers(self, workers):
    for w in workers:
      self.addWorker(w)


  def removeWorker(self, workerID):
    """
      Removes worker from worker list.
    """
    for w in self._workers:
      if w.workerID == workerID:
        if len(w.assignedTasks) == 0:
          self._workers.remove(w)
          self._workersQ.removeWorker(w)
          return
        else:
          raise UnfinishedTasksHeldByWorkerException
    raise UnkownWorkerException


  def assignTasksToWorkers(self):
    tasksToPutIntoSet = []
    for task in self._taskSet:
      try:
        # attempt to assign worker task by normal means.
        self._assignTaskToAnyWorkerOrFail(task)
      except UnassignableTaskException:
        # the task cannot be assigned to worker by normal means
        # try to see if any worker can swap a task.
        try:
          swappedTask = self._assignTaskBySwap(task)
          # as this tas has been swapped we must put it back
          # into the task set immeadiately for re-assignment.
          self._taskSet.add(swappedTask)
        except UnassignableTaskException:
          # no worker could assign task by any means.
          # put back into task set for processing later when worker
          # become available.
          tasksToPutIntoSet.append(task)
          if task not in self._unassignedTasks:
            self._unassignedTasks.append(task)
    for task in tasksToPutIntoSet: # put all unassigned tasks back into set.
      self._taskSet.add(task)


  def _assignTaskToAnyWorkerOrFail(self, task):
    """
      Attempts to assign a task to a worker.
    """
    maxTasksAchievable = self._workersQ.maxTasksAchievable()
    for _ in range(0, maxTasksAchievable):
      # get next worker
      worker = self._workersQ.nextWorker()
      # check if worker has reached limit.
      if not worker.hasReachedTaskLimit() and worker.availableInPeriod(task.release, task.deadline):
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


  def _assignTaskBySwap(self, task):
    """
      Attempts to assign a task by swapping it with another because
      it has an earlier release, this should only be called when it is
      known that all worker have been assigned as many tasks as possible.
      @param task: the task to assign by swapping with another if possible.
      @return Task the task that was swapped.
    """
    maxTasksAchievable = self._workersQ.maxTasksAchievable()
    for _ in range(0, maxTasksAchievable):
      # get next worker
      worker = self._workersQ.nextWorker()
      # first check if worker is actually available in period.
      if worker.availableInPeriod(task.release, task.deadline):
        if worker.hasReachedTaskLimit(): # if worker if full, try see if he can swap.
          # check if any task can be swapped.
          swappableTask = worker.findSwappableTask(task)
          if swappableTask:
            # unassign the task that can be swapped.
            worker.unassignTask(swappableTask.taskID)
            # assign the earlier release task
            worker.assignTask(task)
            task.assignWorker(weakref.ref(worker)())
            # remove swappableTask from assigned tasks
            self._unassignedTasks.append(swappableTask)
            self._assignedTasks.remove(swappableTask)
            # remove the employee who was assigned this task.
            swappableTask.unassignWorker()
            # put the newly assigned task in assignedTasks
            self._unassignedTasks.remove(task)
            self._assignedTasks.append(task)
            return swappableTask # task has been assigned return from method
          else:
            continue # try next worker.
      else:
        continue # worker not available in the period to complete the task, try next one.
    raise UnassignableTaskException
