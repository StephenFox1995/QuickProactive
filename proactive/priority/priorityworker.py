from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta

class PriorityWorker(object):
  def __init__(self, fd, businessID, queue, refresh=5000):
    self.__fd = fd
    self._businessID = businessID
    self._queue = queue
    self._refresh = IntervalTrigger(seconds=(refresh / 1000))
    self._scheduler = BlockingScheduler()
    self._begin()

  def _updateFileWithPriorities(self):
    serializedQueue = self._queue.serialize()
    print(serializedQueue)

  def _begin(self):
    job = self._scheduler.add_job(self._updateFileWithPriorities, trigger=self._refresh)
    self._scheduler.start()
    


