import googlemaps
import json
from coord import coordinate
from gmapsresponse import GmapsResponse



class Travel(object):
  def __init__(self, gmapsKey):
    self._gmapsKey = gmapsKey
    self._gmaps = googlemaps.Client(key=self._gmapsKey)
  
  def duration(self, orig, dest, mode="walking", show="text"):
    return GmapsResponse(
      self._gmaps.distance_matrix(orig, dest, mode=mode)
    ).duration(show)
    
  
  def distance(self, orig, dest, mode="walking", show="text"):
    return GmapsResponse(
      self._gmaps.distance_matrix(orig, dest, mode=mode)
    ).distance(show)








