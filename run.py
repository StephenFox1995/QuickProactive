from proactive import Travel
from proactive.travel import metric
from proactive import coordinate
from proactive import Config
from proactive import Order
from proactive import OrderPriorityQueue
from proactive import PriorityWorker
from proactive import PriorityDB

if __name__ == "__main__":
  config = Config()
  gmapsKey = config.read([config.GMAPS_KEY])[0]
  mongo = config.read([config.DATABASES])[0][0]

  travel = Travel(gmapsKey)
  businessLocation = coordinate("53.346916", "-6.279328")
  testlocation1 = coordinate("53.345376", "-6.279931")
  testLocation2 = coordinate("53.344159", "-6.276262")
  testLocation3 = coordinate("53.343327", "-6.27432")

  test1deadline = travel.find(businessLocation, testlocation1, metric.DURATION, measure="value")
  test2deadline = travel.find(businessLocation, testLocation2, metric.DURATION, measure="value")
  test3deadline = travel.find(businessLocation, testLocation3, metric.DURATION, measure="value")

  orderOne = Order(id=1, deadline=test1deadline, profit=100, processing=300)
  orderTwo = Order(id=2, deadline=test2deadline, profit=20, processing=354)
  orderThree = Order(id=3, deadline=test3deadline, profit=12, processing=200)

  orders = [orderOne, orderTwo, orderThree]
  priority = OrderPriorityQueue(orders)
  
  db = PriorityDB(mongo["uri"], mongo["port"], mongo["database"], mongo["username"], mongo["password"])
  db.connect()
  worker = PriorityWorker(db, "test1234", priority)
  worker.begin()
  
  
