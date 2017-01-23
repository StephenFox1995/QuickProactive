from prioritized import Prioritized
import json


"""
j = (r,d,p,w) 
r - release time
d - deadline
p - processing time
w - weight profit.

j = (r,d,p,w)
r - release time
d - deadline
p - processing time
w - weight profit

Assume: p = d - r
"""
class Order(Prioritized):
   #Constructor (should only be invoked with keyword parameters)
  def __init__(self, id, release, deadline, profit, processing=None):
    self.id = id
    self.release = release
    self.deadline = deadline
    self.profit = profit
    if processing == None:
      self.processing = self.processingTime(self.deadline, self.release)
    
  def processingTime(self, deadline, release):
    return deadline - release
  
  def priority(self):
    return self.processing
  
  def __lt__(self, other):
    return self.priority() < other.priority()
  
  def asDict(self):
    return {
      "id": self.id,
      "release": self.release,
      "deadline": self.deadline,
      "profit": self.profit,
      "processing": self.processing
    }



