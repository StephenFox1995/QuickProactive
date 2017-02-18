from .period import Period

class Conflict(object):
  """
    A data structure that holds all tasks that conflict at a given time.
  """
  def __init__(self, intervals):
    self._intervals = list(intervals)
    self._status = None
    self._availableWorkers = None
    self._workersNeeded = None


  @property
  def period(self):
    begin = self._intervals[0].begin
    end = self._intervals[0].end
    for interval in self._intervals:
      # get the earliest begin time
      if interval.begin < begin:
        begin = interval.begin
      # get the earliest begin time
      if interval.end > end:
        end = interval.end
    return Period(begin, end)


  @property
  def status(self):
    """
      The status of this conflict:
        - ok
        - busy
        - warning
    """
    return self._status


  @status.setter
  def status(self, status):
    self._status = status


  @property
  def availableWorkers(self):
    """
      The available workers for this conflict.
    """
    return self._availableWorkers


  @availableWorkers.setter
  def availableWorkers(self, availableWorkers):
    self._availableWorkers = availableWorkers
    self._setStatus()

  @property
  def workersNeeded(self):
    return self._workersNeeded


  @workersNeeded.setter
  def workersNeeded(self, workersNeeded):
    self._workersNeeded = workersNeeded
    self._setStatus()


  def _setStatus(self):
    if self._workersNeeded and self._availableWorkers:
      if self._workersNeeded > self._availableWorkers:
        self._status = "warning"
      elif self._workersNeeded == self._availableWorkers:
        self._status = "busy"
      else:
        self._status = "ok"


  def asDict(self):
    return {
      "workersNeeded": self._workersNeeded,
      "begin": self.period.begin,
      "end": self.period.end,
      "availableWorkers": self._availableWorkers,
      "status": self._status
    }


  def __iter__(self):
    return iter(self._intervals)


  def __str__(self):
    string = "Conflicts: <"
    for interval in self._intervals:
      string += str(interval)
    string += ">"
    return string


  def __len__(self):
    return len(self._intervals)




class ConflictSet(object):
  """
    A data structure to hold all conflicts for a given task set.
  """
  def __init__(self, conflicts):
    self._conflicts = list(conflicts)


  def all(self):
    return self._conflicts


  def allLessThanOrEqual(self, value):
    conflicts = []
    for conflict in self._conflicts:
      if len(conflict) <= value:
        conflicts.append(conflict)
    return conflicts


  def allGreaterThan(self, value):
    conflicts = []
    for conflict in self._conflicts:
      if len(conflict) > value:
        conflicts.append(conflict)
    return conflicts


  def max(self):
    maxConflict = None
    maxSize = 0
    for conflict in self._conflicts:
      if len(conflict) > maxSize:
        maxConflict = conflict
        maxSize = len(conflict)
    return maxConflict


  def flatten(self):
    intervals = []
    for x in self._conflicts:
      for y in x:
        intervals.append(y)
    return intervals


  def asDict(self):
    conflicts = []
    for conflict in self._conflicts:
      intervals = []
      for interval in conflict:
        _interval = {}
        begin = interval.begin.isoformat()
        end = interval.end.isoformat()
        _interval["begin"] = begin
        _interval["end"] = end
        intervals.append(_interval)
      conflicts.append(intervals)
    return conflicts


  def __str__(self):
    string = ""
    for conflict in self._conflicts:
      string += str(conflict) + "\n"
    return string
