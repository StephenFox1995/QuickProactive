from .exceptions import MaxTaskLimitReachedException, UnkownTaskException

class Worker(object):
  def __init__(self, workerID, begin, end, multitask):
    self._id = workerID
    self._begin = begin
    self._end = end
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


  def unassignTask(self, taskID):
    for task in self._assignedTasks:
      if task.taskID == taskID:
        return self._assignedTasks.remove(task)
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
    return begin >= self._begin and end <= self._end


  def __str__(self):
    return self._id
