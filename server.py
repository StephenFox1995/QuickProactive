from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from proactive.config import Configuration
from proactive.priority.exceptions import (
  UnkownTaskException,
  UnfinishedTasksHeldByWorkerException,
  UnkownWorkerException)
from proactive.priority.priorityservice import PriorityService
from proactive.dbs import BusinessDB, OrderDB
from proactive.priority.worker import Worker
from proactive.utils.timeutil import tHour

app = Flask(__name__)
config = Configuration()
mongo = config.read([config.DATABASES])[0][0]
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


def transormWorkerObject(obj):
  # change to datetime format
  beginHour, beginMinute = obj["begin"].split(".")
  endHour, endMinute = obj["end"].split(".")
  obj["begin"] = tHour(int(beginHour), int(beginMinute))
  obj["end"] = tHour(int(endHour), int(endMinute))
  return Worker(
    workerID=obj["id"],
    begin=obj["begin"],
    end=obj["end"],
    multitask=int(obj["multitask"])
  )

@app.route("/beginservice", methods=["POST"])
@cross_origin()
def begin():
  """
    Begins a new service to monitor orders for a business.
    The request should contain a similar body as the following:
    {
	    "business": {
        "id": "58876b6905733be97fb526ad",
        "multitask": 3
      },
      "refresh": 5000
    }
  """
  _json = request.get_json()
  if _json:
    business = _json.get("business")
    businessID = business["id"]
    refresh = _json["refresh"]
    businessDBConn = BusinessDB(
      mongo["uri"],
      mongo["port"],
      mongo["database"],
      mongo["username"],
      mongo["password"]
    )
    businessDBConn.connect()
    business = businessDBConn.read(businessID)
    businessDBConn.close()
    try:
      priorityService.newProcess(
        business=business,
        processID=businessID,
        refresh=refresh
      )
      return jsonify({
        "status": "Success"
      })
    except priorityService.DuplicateProcessException:
      return jsonify({
        "status": "Failed",
        "reason": "Process already exists for id: %s" % businessID
      }), 400
    else:
      return jsonify({
        "status": "Failed"
      }), 500
  else:
    return jsonify({
        "status": "Failed",
        "reason": "No json in body found"
      }), 422


@app.route("/stopservice", methods=["GET"])
@cross_origin()
def stopWorker():
  processID = request.args["id"]
  try:
    priorityService.stopProcess(processID)
    return jsonify({
      "status": "Success",
    })
  except KeyError:
    return jsonify({
      "status": "Failed",
      "reason": ("No process id %s exists." % processID)
    }), 404
  else:
    return jsonify({
      "status": "Failed",
      "reason": "Unkown error occurred."
    }), 500


@app.route("/tasks", methods=["GET"])
@cross_origin()
def priority():
  processID = request.args["id"]
  try:
    process = priorityService.process(processID=processID)
    state = process.taskSetState()
    return jsonify({"state": state})
  except KeyError:
    return jsonify({
      "status": "failed",
      "reason": "No process exist for id %s" % processID
    }), 500


@app.route("/addworkers", methods=["POST"])
@cross_origin()
def addWorkers():
  """
    {
      "business": {
        "id": "58876b6905733be97fb526ad",
        "workers":[
          { "name":"Andrew Worker", "id": "W1234", "multitask": 2, "begin": 13.30, "end": 18.30},
          { "name": "Sinead Worker", "id": "W1234", "multitask": 2, "begin": 09.30, "end": 18.30}
        ]
      },
    }
  """
  _json = request.get_json()
  if _json:
    businessID = _json["business"]["id"]
    workers = _json["business"]["workers"]
    workerInstances = []
    for w in workers:
      workerInstances.append(transormWorkerObject(w))
    try:
      process = priorityService.process(processID=businessID)
      process.addWorkers(workerInstances)
      return jsonify({
        "status": "Success",
      })
    except KeyError:
      return jsonify({
        "status": "failed",
        "reason": "No process exist for id %s" % businessID
      }), 500
  else:
    pass


@app.route("/removetask", methods=["POST"])
@cross_origin()
def removeTask():
  """
  {
    "business": {
      "id": "58876b6905733be97fb526ad"
    },
    "taskID": "487487942789"
  }
  """
  _json = request.get_json()
  if _json:
    businessID = _json["business"]["id"]
    taskID = _json["taskID"]
    try:
      process = priorityService.process(processID=businessID)
      taskManager = process.taskManager
      taskManager.finishTask(taskID)
      taskManager.assignTasksToWorkers()
      return jsonify({
        "status": "Success",
      })
    except (KeyError, UnkownTaskException) as e:
      return jsonify({
        "status": "Failed",
        "reason": e.message
      }), 500


@app.route("/workers", methods=["GET"])
@cross_origin()
def getWorkers():
  try:
    businessID = request.args["id"]
    process = priorityService.process(processID=businessID)
    taskManager = process.taskManager
    workers = taskManager.workers
    response = {"workers": []}
    for w in workers:
      response["workers"].append(w.asDict())
    return jsonify(response)
  except KeyError:
    return jsonify({
      "status": "Failed",
      "reason": "No process exist for id %s" % businessID
    }), 500


@app.route("/workers", methods=["DELETE"])
@cross_origin()
def removeWorkers():
  try:
    businessID = request.args["id"]
    workerID = request.args["workerID"]
    process = priorityService.process(processID=businessID)
    taskManager = process.taskManager
    taskManager.removeWorker(workerID)
    return jsonify({
      "status": "Success",
      "reason": "Worker removed"
    }), 200
  except KeyError:
    return jsonify({
      "status": "Failed",
      "reason": "No process exist for id %s" % businessID
    }), 500
  except UnfinishedTasksHeldByWorkerException:
    return jsonify({
      "status": "Failed",
      "reason": "Tasks still assigned to worker",
    }), 500
  except UnkownWorkerException:
    return jsonify({
      "status": "Failed",
      "reason": "Uknown worker",
    }), 500

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=6566)
