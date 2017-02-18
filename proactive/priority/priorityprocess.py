import logging
from apscheduler.schedulers.background import BackgroundScheduler
from proactive.config import Configuration
from proactive.travel import Travel, Metric
from proactive.businessobjects.order import Order
from .taskmanager import TaskManager
from .taskunit import TaskUnit


class PriorityProcess(object):
  def __init__(self, business, workers, ordersDBConn, refresh=5000):
    """
      @param businessID:(str) Object will all business info.
      @param workers:(list) A list of worker objects.
      @param ordersDBConn:(db.prioritydb.PriorityDB) Database connection to read orders from.
      @param refresh:(int) - milliseconds: How often the database should be read to when checking
        for new orders. How often the database should be written to with the current state of the
        priority queue.
    """
    self._business = business
    self._businessCoordinates = business.coordinates
    self._taskManager = TaskManager((business.period.begin, business.period.end))
    self._taskManager.addWorkers(workers)
    self._ordersDBConn = ordersDBConn
    self._refresh = refresh
    self._config = Configuration()
    self._travel = Travel(gmapsKey=self._config.read([Configuration.GMAPS_KEY])[0])
    self.__scheduler = BackgroundScheduler()
    self.__orderStore = []

  @property
  def taskManager(self):
    return self._taskManager

  @property
  def tasks(self):
    tasks = []
    for task in self._taskManager.assignedTasks:
      tasks.append(task.asDict())
    return tasks

  def run(self):
    logging.basicConfig()
    self.__scheduler.add_job(self.__monitor, 'interval', seconds=self._refresh/1000)
    self.__scheduler.start()

  def stop(self):
    self.__scheduler.shutdown()

  def __monitor(self):
    """
      Monitors the unprocessed orders and keeps the queue attribute
      in order according to how the orders should be released.
    """
    orders = self.__readUnprocessedOrders(self.__orderStore)
    for order in orders:
      orderObj = Order(
        orderID=str(order["id"]),
        status=order["status"],
        processing=order["processing"],
        customerCoordinates=order["coordinates"],
        travelMode=order["travelMode"],
        createdAt=order["createdAt"],
        cost=order["cost"],
        products=order["products"]
      )
      self.__orderStore.append(orderObj) # add to internal storage.
      deadline = self._customerArrivalTime(orderObj.customerCoordinates, orderObj.travelMode)
      task = TaskUnit(
        createdAt=orderObj.createdAt,
        deadline=deadline,
        profit=orderObj.cost,
        processing=orderObj.processing,
        taskID=orderObj.orderID,
        data=orderObj
      )
      self._taskManager.addTask(task)
    self._taskManager.assignTasksToWorkers()

  def __readUnprocessedOrders(self, excluding):
    return self._ordersDBConn.read(self._business.businessID, excluding)

  def _customerArrivalTime(self, customerCoordinates, travelMode):
    return self._travel.find(
      self._businessCoordinates,
      customerCoordinates,
      Metric.DURATION,
      mode=travelMode,
      measure="value"
    )

  def taskSetState(self):
    state = {
      "assignedTasks": {},
      "unassignedTasks": {},
      "conflicts": {
        "sets": [],
        "utilization": []
      },
    }
    conflicts = self._taskManager.taskSet.findConflicts()[0]
    state["conflicts"]["sets"] = conflicts.asDict()
    state["conflicts"]["utilization"] = []
    conflictAnalysis = self._taskManager.analyseWorkersForNeededTaskSet(multitask=2)[0]
    nonConflictAnalysis = self._taskManager.analyseWorkersForNeededTaskSet(multitask=2)[1]
    for conflict in conflictAnalysis:
      state["conflicts"]["utilization"].append(conflict.asDict())
    for nonConflict in nonConflictAnalysis:
      state["conflicts"]["utilization"].append(nonConflict.asDict())

    state["assignedTasks"] = map(lambda t: t.asDict(), self._taskManager.assignedTasks)
    state["unassignedTasks"] = map(lambda t: t.asDict(), self._taskManager.unassignedTasks)
    return state

  def addWorkers(self, workers):
    self._taskManager.addWorkers(workers)
