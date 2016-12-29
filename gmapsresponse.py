import json
"""
  Encapusulates a response from the Google Maps API, specifically the Distance Matrix API.
  Exposes common methods which may be useful for extracting information from the response.
"""
class GmapsResponse(object):
  def __init__(self, gmapsResponse):
    self.dict = gmapsResponse
    if self.dict["status"] != "OK":
      raise Exception("Status was not OK, status=%s" % self.dict["status"])

  def duration(self, show):
    return self.dict["rows"][0]["elements"][0]["duration"][show]
    
  def distance(self, show):
    return self.dict["rows"][0]["elements"][0]["distance"][show]