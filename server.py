import json
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from proactive.config import Configuration
from proactive.priority.priorityservice import PriorityService
from proactive.dbs import BusinessDB, OrderDB


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



@app.route("/beginWorker", methods=["POST"])
@cross_origin()
def beginWorker():
  """
    Runs a new worker to monitor orders for a business.
    {
      "business": {
        id: "test1234"
      },
      refresh: 5000
    }
  """
  json_ = request.get_json()

  if json_:
    business = json_.get("business")
    businessID = business["businessID"]
    refresh = json_["refresh"]

    # Setup connection to orders database.
    # TODO: maybe get rid of this and make client send business details.
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
      priorityService.newWorker(business=business, workerID=businessID, refresh=refresh)
      return jsonify({
        "status": "Success"
      })
    except priorityService.DuplicateWorkerException:
      return jsonify({
        "status": "Failed",
        "reason": "Worker already exists for id: %s" % businessID
      })
    else:
      return jsonify({
        "status": "Failed"
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


