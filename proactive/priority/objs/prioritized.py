from abc import ABCMeta, abstractmethod

class Prioritized:
  __metaclass__ = ABCMeta

  @abstractmethod
  def priority(self):
    pass