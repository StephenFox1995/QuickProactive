from abc import ABCMeta, abstractmethod

class Prioritized(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def priority(self):
    pass

  @abstractmethod
  def __lt__(self, other):
    pass

  @abstractmethod
  def asDict(self):
    pass
