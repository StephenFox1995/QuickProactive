import json
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
  
  def duration(self, measure):
    return self.dict["rows"][0]["elements"][0]["duration"][measure]
    
  def distance(self, measure):
    return self.dict["rows"][0]["elements"][0]["distance"][measure]