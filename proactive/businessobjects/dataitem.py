from abc import ABCMeta, abstractmethod

class DataItem(object):
  """
    Abstract class for any concrete class that can be of 'priority', in other words,
    that would represent some priority if it were in a list etc.
  """
  __metaclass__ = ABCMeta

  @abstractmethod
  def asDict(self):
    pass
