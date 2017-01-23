from db import Database


class PriorityDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(PriorityDB, self).__init__(uri, port, dbName, user, password)
    self.__clients = []

  def write(self, businessID, priority):
    """
      Writes the priority queue to MongoDB.
      If a priority queue already exists for the paticular business then it will be replaced.
      
      @param businessID:(str) The id of the business the queue belongs to.

      @param priority:(dict) A dict representation of the priority queue.
    """
    if businessID in self.__clients:
      return self.database.priority.replace_one({"businessID": businessID}, priority)
    else:
      self.__clients.append(businessID)
      return self.database.priority.insert_one(priority)


  def read(self, businessID):
    return self.database.priority.find({"businessID": businessID})