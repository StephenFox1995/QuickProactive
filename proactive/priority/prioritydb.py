from db import Database


class PriorityDB(Database):
  def write(self, priority):
    result = self.database.priority.insert_one(priority)
    print(result)

  def read(self):
    pass