from intervaltree import IntervalTree

class TaskManager(object):
  def __init__(self, period):
    self.__tasks = []
    self.__intervalTree = IntervalTree()
    self.__start = period[0]
    self.__end = period[1]

  def addTask(self, task):
    self.__tasks.append(task)
    self.__addTaskToTree(task)

  def addTasks(self, tasks):
    for task in tasks:
      self.__tasks.append(task)
      self.__addTaskToTree(task)

  def __addTaskToTree(self, task):
    self.__intervalTree.addi(
      begin=task["release"],
      end=task["deadline"],
      data=task["id"]
    )


  def findConflicts(self, threshold):
    begin = self.__intervalTree.begin()
    end = self.__intervalTree.end()
    underThresholdConflicts = []
    overThresholdConflict = []

    intervals = sorted(self.__intervalTree[begin:end])
    for interval in intervals:
      _intervals = self.__intervalTree[interval.begin:interval.end]
      if len(_intervals) > 1: # theres a conflict
        if len(_intervals) <= threshold:
          if _intervals not in underThresholdConflicts:
            underThresholdConflicts.append(_intervals)
        else:
          if _intervals not in overThresholdConflict:
            overThresholdConflict.append(_intervals)
    return (underThresholdConflicts, overThresholdConflict)

