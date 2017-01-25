from database import Database
from ..priority.order import Order
from bson import ObjectId

class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, businessID):
    super(OrderDB, self).read()
    return self._database.orders.find({
      "businessID": ObjectId(businessID), 
      "status": Order.Status.UNPROCESSED
    })