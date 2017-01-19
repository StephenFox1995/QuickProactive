
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


order1 = {
  "release": 20,
  "processing": 245, 
  "deadline": 231,
  "profit":30
}
order2 = {
  "release": 20,
  "processing": 245, 
  "deadline": 209,
  "profit": 50
}


def processingTime(order):
  # processing = deadline - release
  order["processing"] = order["deadline"] - order["release"]
  return order


def rank():
  pass


if __name__ == "__main__":
  pass