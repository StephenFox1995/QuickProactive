import json
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from proactive.config import Configuration
from proactive.priority.priorityservice import PriorityService
from proactive.dbs import BusinessDB, OrderDB
from proactive.priority.worker import Worker

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
  return Worker(
    workerID=obj["id"],
    multitask=obj["multitask"]
  )

@app.route("/beginService", methods=["POST"])
@cross_origin()
def begin():
  """
    Begins a new service to monitor orders for a business.
    The request should contain a similar body as the following:
    {
	    "business": {
		  "id": "58876b6905733be97fb526ad",
        "workers":[
          { "name":"Andrew Worker", "id": "W1234", "multitask": 2},
          { "name": "Sinead Worker", "id": "W1234", "multitask": 2 }
        ]
      },
   	  "refresh": 5000
    }
  """
  _json = request.get_json()
  if _json:
    business = _json.get("business")
    businessID = business["id"]
    refresh = _json["refresh"]
    workers = business["workers"]
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

    workerInstances = []
    for w in workers:
      workerInstances.append(transormWorkerObject(w))

    try:
      priorityService.newProcess(
        business=business,
        processID=businessID,
        workers=workerInstances,
        refresh=refresh
      )
      return jsonify({
        "status": "Success"
      })
    except priorityService.DuplicateProcessException:
      return jsonify({
        "status": "Failed",
        "reason": "Process already exists for id: %s" % businessID
      })
    else:
      return jsonify({
        "status": "Failed"
      })
  else:
    return jsonify({
        "status": "Failed",
        "reason": "No json in body found"
      })


@app.route("/stopWorker", methods=["GET"])
@cross_origin()
def stopWorker():
  workerID = request.args["id"]
  try:
    priorityService.stopWorker(workerID)
    return Response(response="Success!")
  except KeyError:
    return Response(response="Failed!")

@app.route("/queue")
@cross_origin()
def priority():
  workerID = request.args["id"]
  try:
    queueState = json.dumps(priorityService.workerQueueState(workerID=workerID))
    return Response(response=queueState)
  except KeyError:
    return Response(response="Failed!")


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=6566)


