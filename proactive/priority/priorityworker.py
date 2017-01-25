from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta
from db import Database
import logging

class PriorityWorker(object):
  def __init__(self, dbConnection, businessID, queue, refresh=5000):
    """
      @param dbConnection:(priority.PriorityDB) Connection to the database where 
        the priority queue will be written to periodically.

      @param businessID:(str) The id of the business.

      @param queue:(proactive.priority.Priority) OrderPriorityQueue class.

      @param refresh:(int) - milliseconds: How often the database should be read to when checking
        for new orders. How often the database should be written to with the current state of the
        priority queue.
    """
    logging.basicConfig() # Set logger.
    self._dbConnection = dbConnection
    self._businessID = businessID
    self._queue = queue
    self._refresh = IntervalTrigger(seconds=(refresh / 1000))
    self._scheduler = BlockingScheduler()
  
  
  def _updateDatabaseWithPriorities(self):
    queueAsDict = self._queue.asDict()
    queueAsDict["businessID"] = self._businessID
    result = self._dbConnection.write(self._businessID, queueAsDict)
    print(result)
    
  
  def begin(self):
    job = self._scheduler.add_job(self._updateDatabaseWithPriorities, trigger=self._refresh)
    self._scheduler.start()
    


