from .priorityprocess import PriorityProcess

class PriorityService(object):
  class DuplicateProcessException(Exception):
    pass

  def __init__(self, orderDBConn):
    self._orderDBConn = orderDBConn
    self.__processes = {}

  def newProcess(self, business, workers, processID, refresh=5000):
    """
      Creates a new priorityprocess.PriorityProcess to periodically
      calculate the priority of new orders.
      @param business:(Business) Object that contains 'businessID'
      @param workers:(list) A list of worker objects.
      @param refresh:(int)  The refresh rate in milliseconds, i.e
                            how often the service will run.
    """
    if processID in self.__processes:
      raise self.DuplicateProcessException("Process already exists with that id.")
    process = PriorityProcess(
      business=business,
      ordersDBConn=self._orderDBConn,
      workers=workers,
      refresh=refresh
    )
    self.__processes[processID] = process
    process.run()

  def processState(self, processID):
    process = self.__processes[processID]
    return process.tasks

  @property
  def process(self, processID):
    return self.__processes[processID] # throws KeyError if doesn't exist.

  def stopProcess(self, processID):
    self.__processes[processID].stop()
    del self.__processes[processID]
