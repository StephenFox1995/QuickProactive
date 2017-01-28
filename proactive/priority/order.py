from datetime import datetime
from dateutil import parser as dateparser
from proactive.utils import timeutil
from .prioritized import Prioritized
from . import release



class Order(Prioritized):
  class Status(object):
    UNPROCESSED = "unprocessed"
    PROCESSED = "processed"

   #Constructor (should only be invoked with keyword parameters)
  def __init__(self, orderID, createdAt, deadline, profit, processing):
    """
      @param orderID:(str) The id of the order.
      @param deadline:(int) The number of seconds for the deadline of this order.
      @param profit:(double) The profit from this order.
      @param processing:(int) The time in seconds it would take to process this order.
      @param createdAt:(datetime.datetime) The time the order was made.

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
    """
    self.id = orderID
    self.profit = profit
    # Set time attrs so deadline, release etc are calculated correctly.
    self.createdAt = createdAt
    self.deadline = deadline
    self.deadlineISO = timeutil.addSeconds(datetime.now(), self.deadline).isoformat()
    self.processing = processing
    # Re-calculate the time left to process.
    self.timeLeftToProcess = release.timeToProcess(self)
    # Re-calculate the time until release.
    self.release = release.releaseAt(self.deadline, self.processing, self.createdAt)
    self.releaseISO = self.release.isoformat()


  def priority(self):
    return dateparser.parse(self.deadlineISO)

  def __lt__(self, other):
    return self.priority() < other.priority()

  def asDict(self):
    return {
      "id": self.id,
      "releaseISO": self.releaseISO,
      "deadlineISO": self.deadlineISO,
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing,
      "timeLeftToProcess": self.timeLeftToProcess
    }
