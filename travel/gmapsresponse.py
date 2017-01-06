import json
import find as Find

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


  def matrixInfo(self, find, measure, row=0):
    """
      Extracts the appropriate information from a Google Maps Matrix API response.

      @param find:(str) See find() method in Travel class for further info.

      @param measure:(str) See find() method in Travel class for further info.
    """
    if find == Find.DURATION or find == Find.DISTANCE:
      return self.dict["rows"][row]["elements"][0][find][measure]
    else:
      raise ValueError("Uknown %s information to find" % find)
