from intervaltree import IntervalTree

class ConflictSet(object):
  def __init__(self, conflicts):
    self._conflicts = conflicts

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

  def flatten(self):
    intervals = []
    for x in self._conflicts:
      for y in x:
        intervals.append(y)
    return intervals



class TaskManager(object):
  def __init__(self, period):
    self.__tasks = []
    self.__intervalTree = IntervalTree()
    self.__start = period[0]
    self.__end = period[1]

  def addTask(self, task):
    if task.deadline > self.__end:
      raise Exception(
        "Cannot process this task as it's deadline is %s is after %s"
        % (task.deadline, self.__end)
      )
    self.__tasks.append(task)
    self.__addTaskToTree(task)

  def addTasks(self, tasks):
    for task in tasks:
      self.__tasks.append(task)
      self.__addTaskToTree(task)

  def __addTaskToTree(self, task):
    self.__intervalTree.addi(
      begin=task.release,
      end=task.deadline,
      data=task.taskID
    )

  def findConflicts(self):
    """
      Finds all the conflicts within the tasks set.
      A conflict being, any two or more tasks that need
      to be proccessed at some point simultaneously.
      In terms of an interval tree, the two task times 'overlap'.

      This method finds all the conflicts of the current task set
      held by this class.
    """
    begin = self.__intervalTree.begin()
    end = self.__intervalTree.end()
    conflicts = []
    intervals = sorted(self.__intervalTree[begin:end])
    for interval in intervals:
      _intervals = self.__intervalTree[interval.begin:interval.end]
      if len(_intervals) > 1: # theres a conflict
        if _intervals not in conflicts:
          conflicts.append(_intervals)
    return ConflictSet(conflicts)

  def findNonConflicts(self):
    conflicts = self.findConflicts().flatten()
    return self.__intervalTree.difference(conflicts).items()

