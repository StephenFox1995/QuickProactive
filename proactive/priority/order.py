from prioritized import Prioritized
from datetime import datetime, timedelta

class Order(Prioritized):
   #Constructor (should only be invoked with keyword parameters)
  def __init__(self, id, deadline, profit, processing, release=None):
    """
      @param id:(str) The id of the order.
      @param release:(int) The number of seconds when this order needs to be released.
      @param deadline:(int) The number of seconds for the deadline of this order.
      @param profit:(double) The profit from this order.
      @param processing:(int) The time in seconds it would take to process this order.
    
      j = (r,d,p,w) 
      r - release time
      d - deadline
      p - processing time
      w - weight profit.

      j = (r,d,p,w)
      r - release time
      d - deadline
      p - processing time
      w - weight profit

      Assume: p = d - r
    """
    self.id = id
    self.deadline = deadline
    self.profit = profit
    self.processing = processing
    self.timeLeftToProcess = self._timeLeftToProcess(self.deadline, self.processing)
    if release == None:
      self.release = self._releaseAt(self.timeLeftToProcess, self.deadline, self.processing)


  def _timeLeftToProcess(self, deadline, processing):
    """
      Calculate the time left to process an order based on 
      t = deadline - processing
    """
    return deadline - processing
  
  def _releaseAt(self, timeLeftToProcess, deadline, processing, buff=0):
    """
      The release time is calculate in the following way.
      r = deadline - processing - buff, where:
        deadline: is the time the order should be processed by.
        processing: the time it will take to process the order.
        buff: is a buffer period which can be seen as extra time to process.
              For example if processing is 15 mins and buff is 2 mins,
              then the release for this order will be two minutes earlier,
              than the 15 minute period, so release will be 17 mins earlier than deadline.
     
     @param timeLeftToProcess:(int) The time left to process the order (seconds)

     @param deadline:(int) The number of seconds left until the deadline.

     @param processing:(int) The number of seconds it will take to process the order

     @param buff:(int) The buffer period (seconds)
    """
    # If the time to process the order is greater
    # than the deadline, this is urgent and the order
    # should be released ASAP.
    if timeLeftToProcess > deadline - buff: 
      return datetime.now()
    
    deadlineTimeFormat = datetime.now() + timedelta(seconds=deadline)
    return deadlineTimeFormat - (timedelta(seconds=processing) - timedelta(seconds=buff))
    


  def priority(self):
    return 10
  
  def __lt__(self, other):
    return self.priority() < other.priority()
  
  def asDict(self):
    return {
      "id": self.id,
      "release": self.release.isoformat(),
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing,
      "timeLeftToProcess": self.timeLeftToProcess
    }



