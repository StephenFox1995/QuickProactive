from bson.objectid import ObjectId
from .database import Database


class BusinessDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(BusinessDB, self).__init__(uri, port, dbName, user, password)

  def read(self, businessID):
    super(BusinessDB, self).read()
    business = self._database.businesses.find_one({"_id": ObjectId(businessID)})
    business["id"] = str(business.pop("_id")) # rename _id to id and change to str.
    return business
