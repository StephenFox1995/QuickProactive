from database import Database

class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, business):
    super(OrderDB, self).read()
    return self._database.order.find({"businessID": "businessID"})