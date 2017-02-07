from .priorityprocess import PriorityProcess
from .business import Business

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
      @param business:(object) Object that contains 'businessID'
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

  def workerQueueState(self, workerID):
    """
      Gets a workers queue state.
      The state is gotten by invoking:
        worker.currentQueueState()

      @param workerID:(string) The id of the worker.
    """
    worker = self.__processes[workerID] # throws KeyError if doesn't exist.
    return worker.currentQueueState()

  @property
  def process(self, processID):
    return self.__processes[processID] # throws KeyError if doesn't exist.

  def stopProcess(self, processID):
    self.__processes[processID].stop()
    del self.__processes[processID]
