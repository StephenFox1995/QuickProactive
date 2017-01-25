from database import Database
from ..priority.order import Order
from bson import ObjectId

class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, businessID):
    super(OrderDB, self).read()
    orders = self._database.orders.aggregate([
      { 
        "$match": {
          "businessID": ObjectId(businessID), 
          "status": Order.Status.UNPROCESSED
        }
      },
      { 
        "$project": {
          "_id": 0,
          "id": "$_id",
          "businessID": 1,
          "userID": 1,
          "cost": 1,
          "location": 1,
          "processing": 1,
          "status": 1
        }
      }
    ])
    return orders
    
    
