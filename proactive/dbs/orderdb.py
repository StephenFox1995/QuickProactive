from bson import ObjectId
from proactive.businessobjects.order import Order
from .database import Database

class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, businessID, excluding=None):
    """
      Read all orders for a business.
      @param businessID: The id of the business.
      @param excluding: A list of orderIDs to not return.
    """
    super(OrderDB, self).read()
    excluded = map(lambda e: ObjectId(e.orderID), excluding)
    pipeline = [
      {
        "$match": {
          "businessID": ObjectId(businessID),
          "status": Order.Status.UNPROCESSED,
          "_id": {"$nin": excluded}
        }
      },
      {
        "$project": {
          "_id": 0,
          "id": "$_id",
          "createdAt": 1,
          "businessID": 1,
          "userID": 1,
          "travelMode": 1,
          "cost": 1,
          "coordinates": 1,
          "processing": 1,
          "status": 1,
          "products": 1
        }
      }
    ]
    return self._database.orders.aggregate(pipeline)
