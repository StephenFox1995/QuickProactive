from . import metric as Metric

"""
  Encapusulates a response from the Google Maps API, specifically the Distance Matrix API.
  Exposes common methods which may be useful for extracting information from the response.
"""
class GmapsResponse(object):
  def __init__(self, gmapsResponse):
    self.dict = gmapsResponse
    status = gmapsResponse["status"]
    if status != "OK":
      raise Exception("Status was not OK, status=%s" % self.dict["status"])


  def matrixInfo(self, metric, measure, row=0):
    """
      Extracts the appropriate information from a Google Maps Matrix API response.

      @param metric:(str) The metric to extract.

      @param measure:(str) The measurement.
    """
    if metric == Metric.DURATION or metric == Metric.DISTANCE:
      return self.dict["rows"][row]["elements"][0][metric][measure]
    else:
      raise ValueError("Uknown mertic: %s" % metric)
