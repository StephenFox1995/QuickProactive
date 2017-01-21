from prioritized import Prioritized

class Order(Prioritized):
   #Constructor (should only be invoked with keyword parameters)
  def __init__(self, release, deadline, profit, processing=None):
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

# j = (r,d,p,w) 
# r - release time
# d - deadline
# p - processing time
# w - weight profit.

"""
j = (r,d,p,w)
r - release time
d - deadline
p - processing time
w - weight profit

Assume: p = d - r
"""

