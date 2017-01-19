from prioritized import Prioritized

class Order(Prioritized):
  def __init__(self, release, deadline, profit, processing=None):
    self.release = release
    self.deadline = deadline
    self.profit = profit
    if processing == None:
      processing = self.processingTime(self.deadline, self.release)
    
  def processingTime(self, deadline, release):
    return deadline - release
  
  def priority():
    pass
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

