from .exceptions import ExceededWorkerMultitaskLimit

class Worker(object):
  def __init__(self, workerID, multitask):
    self._id = workerID
    self._multitask = multitask
    self._assignedTasks = []

  @property
  def workerID(self):
    return self._id

  @property
  def assignedTasks(self):
    return self._assignedTasks

  @property
  def multitask(self):
    return self._multitask

  def assignTask(self, task):
    if len(self._assignedTasks) == self._multitask:
      raise ExceededWorkerMultitaskLimit(
        "Cannot assign any more tasks to worker: %s", self._id
      )
    else:
      self._assignedTasks.append(task)
