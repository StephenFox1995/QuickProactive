from proactive import Travel
from proactive.travel import metric
from proactive import coordinate
from proactive import Config
from proactive import Order
from proactive import Priority
from proactive import PriorityWorker
from proactive import PriorityDB

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
  cust1deadline = travel.find(coord1, coord2, metric.DURATION, measure="value")
  cust2deadline = travel.find(coord3, coord4, metric.DURATION, measure="value")
  cust3deadline = travel.find(coord5, coord6, metric.DURATION, measure="value")

  orderOne = Order(id=1, deadline=cust1deadline, profit=100, processing=300)
  orderTwo = Order(id=2, deadline=cust2deadline, profit=20, processing=354)
  orderThree = Order(id=3, deadline=cust3deadline, profit=12, processing=400)


  orders = [orderOne, orderTwo, orderThree]
  priority = Priority(orders)
  
  db = PriorityDB(mongo["uri"], mongo["port"], mongo["database"], mongo["username"], mongo["password"])
  db.connect()
  worker = PriorityWorker(db, "test1234", priority)
  worker.begin()
  
  
