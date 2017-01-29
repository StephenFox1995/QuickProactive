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
    self._createdAt = createdAt
    self._deadline = deadline
    self._deadlineISO = timeutil.addSeconds(createdAt, self._deadline).isoformat()
    self._processing = processing
    self._release = release.releaseAt(self.deadline, self._processing, self.createdAt)
    self._releaseISO = self._release.isoformat()
    self._profit = profit
    self._taskID = taskID
    self._item = item

  @property
  def createdAt(self):
    return self._createdAt

  @property
  def deadline(self):
    return self._deadline

  @property
  def processing(self):
    return self._processing

  @property
  def release(self):
    return self._processing

  @property
  def profit(self):
    return self._profit

  @property
  def taskID(self):
    return self._taskID

  @property
  def item(self):
    return self._item

  def __lt__(self, other):
    return self.priority() < other.priority()

  def priority(self):
    return dateparser.parse(self._deadlineISO)

  def asDict(self):
    return {
      "id": self.taskID,
      "releaseISO": self._releaseISO,
      "deadlineISO": self._deadlineISO,
      "deadline": self._deadline,
      "profit": self._profit,
      "processing": self._processing
    }

