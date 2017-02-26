class LateDeadlineException(Exception):
  pass

class MaxTaskLimitReachedException(Exception):
  pass

class UnassignableTaskException(Exception):
  pass

class UnkownTaskException(Exception):
  pass

class DuplicateTaskException(Exception): # when same task is added to task set twice.
  pass

class UnfinishedTasksHeldByWorkerException(Exception):
  pass

class UnkownWorkerException(Exception):
  pass
