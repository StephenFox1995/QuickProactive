from proactive.utils import timeutil
from dateutil import parser as dateparser
from .prioritized import Prioritized
from . import release

class TaskUnit(Prioritized):
  def __init__(self, createdAt, deadline, profit, processing, taskID=None, item=None):
    """
      A task unit is composed of the following:
        t_unit = (r,d,p,w)
        r - release time
        d - deadline
        p - processing time
        w - weight profit.
    """
    self.createdAt = createdAt
    self.deadline = deadline
    self.deadlineISO = timeutil.addSeconds(createdAt, self.deadline).isoformat()
    self.processing = processing
    self.release = release.releaseAt(self.deadline, self.processing, self.createdAt)
    self.releaseISO = self.release.isoformat()
    self.profit = profit
    self.taskID = taskID
    self.item = item


  def __lt__(self, other):
    return self.priority() < other.priority()

  def priority(self):
    return dateparser.parse(self.deadlineISO)

  def asDict(self):
    return {
      "id": self.taskID,
      "releaseISO": self.releaseISO,
      "deadlineISO": self.deadlineISO,
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing
    }

