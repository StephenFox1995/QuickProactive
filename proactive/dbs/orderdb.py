from bson import ObjectId
from proactive.priority.order import Order
from .database import Database


class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, businessID):
    super(OrderDB, self).read()
    pipeline = [
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
          "createdAt": 1,
          "businessID": 1,
          "userID": 1,
          "cost": 1,
          "coordinates": 1,
          "processing": 1,
          "status": 1
        }
      }
    ]
    return self._database.orders.aggregate(pipeline)
