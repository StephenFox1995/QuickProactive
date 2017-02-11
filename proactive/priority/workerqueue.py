from Queue import Queue

class WorkerQueue(object):
  def __init__(self):
    self._queue = Queue(maxsize=-1)
    self._workers = []
    self._workersToRemove = []

  def put(self, worker):
    if isinstance(worker, list):
      for w in worker:
        self._queue.put(w)
        self._workers.append(w)
    else:
      self._queue.put(worker)
      self._workers.append(worker)

  def nextWorker(self):
    worker = self._queue.get() # take woker from the queue.
    if worker in self._workersToRemove:
      self._workersToRemove.remove(worker)
      return self.nextWorker()
    self._queue.put(worker) # put the worker to the back of the queue.
    return worker

  def removeWorker(self, worker):
    self._workers.remove(worker)
    self._workersToRemove.append(worker)

  def size(self):
    return self._queue.qsize()

  def maxTasksAchievable(self):
    """
      Calculated the max tasks that can be completed by the
      current workers available.
    """
    maxTasks = 0
    for w in self._workers:
      maxTasks = maxTasks + w.multitask
    return maxTasks

  def __str__(self):
    string = ""
    for w in self._workers:
      string += " " + str(w)
    return string
