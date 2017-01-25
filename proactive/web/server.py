from flask import Flask, Response, request


if __name__ == "__main__":
  app = Flask(__name__)
  app.run(host='0.0.0.0', port=6565, debug=True)


@app.route("/beginObserving", methods=["POST"])
def beginObserving():
"""
  Example of POST request:
  { subject: { businessID: "test1234"} }
"""
  if request.json:
    pass



  

