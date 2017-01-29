from abc import ABCMeta, abstractmethod

class QueueWorker(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def currentQueueState(self):
    pass
