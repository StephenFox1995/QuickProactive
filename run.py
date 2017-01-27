from proactive.config import Configuration
from proactive.priority.priorityservice import PriorityService
from proactive.dbs import BusinessDB, OrderDB

if __name__ == "__main__":
  config = Configuration()
  mongo = config.read([config.DATABASES])[0][0]
  businessID = "58876b6905733be97fb526ad"

  # Setup connection to orders database.
  businessDBConn = BusinessDB(
    mongo["uri"],
    mongo["port"],
    mongo["database"],
    mongo["username"],
    mongo["password"]
  )
  # Get the business from the database.
  businessDBConn.connect()
  business = businessDBConn.read(businessID)

  # Setup connection to orders database.
  orderDBConn = OrderDB(
    mongo["uri"],
    mongo["port"],
    mongo["database"],
    mongo["username"],
    mongo["password"]
  )
  orderDBConn.connect()

  priorityService = PriorityService(orderDBConn)
  priorityService.new(business)



