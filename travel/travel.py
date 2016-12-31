import googlemaps
from coord import coordinate
from gmapsresponse import GmapsResponse
from datetime import datetime


class Travel(object):
  def __init__(self, gmapsKey, rateLimit=20):
    """
      Initialises a new instance of the Travel class
      which can be used for finding travel information
      from one place to another using the Google Maps API.

      @param gmapsKey:(string) The Google Maps API key.

      @param rateLimit:(int) The time to wait until a new request is sent
      if the same origin and destination are used. If different locations are
      used than the previous invocation of #find() then rate limit will not take effect.
    """
    self._gmapsKey = gmapsKey
    self._gmaps = googlemaps.Client(key=self._gmapsKey)
    self._rateLimit = rateLimit
    self._lastOrig = None
    self._lastDest = None
    self._mostRecentRequestTime = None


  def find(self, orig, dest, find=None, mode="walking", measure="value"):
    """
      Method to find some travel information about two different locations.

      @param orig See googlemaps.distance_matrix for correct type.

      @param dest See googlemaps.distance_matrix for correct type.

      @param find:(string) Specify what to find in relation to the two
        locations, currently supported is 'distance', 'duration'

      @param mode:(string) The mode of travel.

      @param measure:(string) Whether to return a text based measure or a correct
        measure according to the value. E.g text=4.32km, value=4.25
    """
    shouldFetch = False
    # New location to find?
    if self._lastOrig != orig and self._lastDest != dest:
      shouldFetch = True
    self._lastOrig = orig
    self._lastDest = dest

    if self._mostRecentRequestTime != None:
      # Check if a new request should be sent, based on the rateLimit value.
      if (datetime.now() - self._mostRecentRequestTime).total_seconds() >= self._rateLimit:
        shouldFetch = True

    if shouldFetch:
      # Send request.
      self._response = GmapsResponse(self._gmaps.distance_matrix(orig, dest, mode=mode))
      # Record the request time
      self._mostRecentRequestTime = datetime.now()

    return self._response.matrixInfo(find, measure)
