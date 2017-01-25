from pymongo import MongoClient
from mongoutil import connString

class Database(object):
  def __init__(self, uri, port, dbName, user=None, password=None):
    self._uri = uri
    self._port = port
    self._dbName = dbName
    self.__user=user
    self.__password=password
    self.__connectionString = connString(uri, port, dbName, user, password)

  def connect(self):
    """
    Connects to the database from the arguments specified in the constructor.
    """
    self.client = MongoClient(self.__connectionString)
    self.database = self.client.get_database(self._dbName)
    del self.__user
    del self.__password
    del self.__connectionString
    
  def close(self):
    """
    Closes the current connection to the database.
    """
    self.client.close()
  
