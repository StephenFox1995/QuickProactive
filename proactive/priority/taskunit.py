from proactive.utils import timeutil
from dateutil import parser as dateparser
from .priority import Priority
from . import release

class TaskUnit(Priority):
  def __init__(self, createdAt, deadline, profit, processing, taskID=None, item=None):
    """
      A task unit is a schedulable piece of work that needs to be completed
      before a deadline. However, as the scheduling is not computer scheduling
      and merely advice to humans when specific tasks should be released/started
      and completed. (Humans can do multiple tasks)

      w1 = 100
      r1 = 14.00
      c1 = 13:00

      w2 = 3
      r2 = 14:05
      c2 = 13:00

      w3 = 40
      r3 = 14:10
      c3 = 14:00
      100/14 + 13
      weight / (release) [createdAt/(sequence)]
      deadline / release + profit
      1. fifo
      2. Priority/adaptive queue

      A TaskUnit is composed of the following properties:
        t_unit = (c, r,d,p,w)
        c - createdAt
        r - release time
        d - deadline
        p - processing time
        w - weight profit.

      @param createdAt:(datetime) The time the task arrived into the system or was made.
      @param deadline:(int) The number of seconds until the deadline.
      @param profit:(double) The potential profit from getting this task finished on on time.
      @param processing:(int) The number of seconds the task will take to process.
      @param taskID:(str) The id of the task.
      @param item:(object) Optionally an TaskUnit can encapsulate another object that
        has a relationship with the unit of work. For example, the most common scenario
        for this applicaiton would be customer orders. An order itself can be viewed
        as a unit of work, however it makes more sense to encapsulate it into a generic form
        i.e this class.
    """
    self._createdAt = createdAt
    self._createdAtISO = createdAt.isoformat()
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
  def createdAtISO(self):
    return self._createdAtISO

  @property
  def deadline(self):
    return self._deadline

  @property
  def deadlineISO(self):
    return self._deadlineISO

  @property
  def processing(self):
    return self._processing

  @property
  def release(self):
    return self._processing

  @property
  def releaseISO(self):
    return self._releaseISO

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
      "processing": self._processing,
      "createdAtISO": self._createdAtISO
    }

