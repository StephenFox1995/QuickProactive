from .exceptions import (
  MaxTaskLimitReachedException,
  UnkownTaskException,
  UnassignableTaskException)

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


  def assignTask(self, task):
    self._assignedTasks.append(task)


  def hasReachedTaskLimit(self):
    return len(self._assignedTasks) >= self._multitask


  def findSwappableTask(self, task):
    """
      Find any task that can be swapped and returns it
      because there release is later than the task passed to the method.
    """
    for _task in self._assignedTasks:
      if task.release < _task.release and not _task.isProcessing():
        return _task

  def availableInPeriod(self, begin, end):
    return begin >= self._begin and end <= self._end


  def __str__(self):
    return self._id
