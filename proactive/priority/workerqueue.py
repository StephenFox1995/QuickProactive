from Queue import Queue

class WorkerQueue(object):
  def __init__(self):
    self._queue = Queue(maxsize=-1)

  def put(self, worker):
    if isinstance(worker, list):
      for w in worker:
        self._queue.put(w)
    else:
      self._queue.put(worker)

  def next(self):
    worker = self._queue.get() # take woker from the queue.
    self._queue.put(worker) # put the worker to the back of the queue.
    return worker

  def size(self):
    return self._queue.qsize()
