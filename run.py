from proactive import Travel
from proactive.travel import metric
from proactive import coordinate
from proactive import Config
from proactive import Order
from proactive import Priority
from proactive import PriorityWorker
from proactive import Database

if __name__ == "__main__":
  config = Config()
  gmapsKey = config.read([config.GMAPS_KEY])[0]
  mongo = config.read([config.DATABASES])[0][0]

  travel = Travel(gmapsKey)
  coord1 = coordinate("53.348418", "-6.2782096")
  coord2 = coordinate("53.3269158", "-6.2793282")
  coord3 = coordinate("53.18418", "-6.1782096")
  coord4 = coordinate("53.3289158", "-6.2793282")
  coord5 = coordinate("53.3269158", "-6.2793282")
  coord6 = coordinate("53.18418", "-6.2793282")
  cust1 = travel.find(coord1, coord2, metric.DURATION, measure="value")
  cust2 = travel.find(coord3, coord4, metric.DURATION, measure="value")
  cust3 = travel.find(coord5, coord6, metric.DURATION, measure="value")
  orderOne = Order(id=1, release=0, deadline=cust1, profit=100)
  orderTwo = Order(id=2, release=0, deadline=cust2, profit=20)
  orderThree = Order(id=3, release=0, deadline=cust3, profit=12)


  orders = [orderOne, orderTwo, orderThree]
  priority = Priority(orders)
  
  # worker = PriorityWorker("s", "1234", priority)
  db = Database(mongo["uri"], mongo["port"], mongo["database"], mongo["username"], mongo["password"])
  db.connect()
  
  
