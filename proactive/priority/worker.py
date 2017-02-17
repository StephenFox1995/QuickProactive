from .exceptions import MaxTaskLimitReachedException, UnkownTaskException

class Worker(object):
  def __init__(self, workerID, multitask):
    self._id = workerID
    self._multitask = multitask
    self._assignedTasks = []
    self._begin = None
    self._end = None

  @property
  def workerID(self):
    return self._id


  @property
  def assignedTasks(self):
    return self._assignedTasks


  @property
  def multitask(self):
    return self._multitask


  def unassignTask(self, task):
    if task in self._assignedTasks:
      self._assignedTasks.remove(task)
    else:
      raise UnkownTaskException("Unkown task")


  def canAssignTask(self):
    return not(len(self._assignedTasks) >= self._multitask)


  def assignTask(self, task):
    if not self.canAssignTask():
      raise MaxTaskLimitReachedException(
        "Cannot assign any more tasks to worker: %s", self._id
      )
    else:
      self._assignedTasks.append(task)


  def availableInPeriod(self, begin, end):
    return self._begin >= begin and self._end <= end


  def __str__(self):
    return self._id
