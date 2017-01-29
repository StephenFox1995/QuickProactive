import googlemaps
from .gmapsresponse import GmapsResponse


class Travel(object):
  class GmapsFactory(object):
    @staticmethod
    def newGmapsClient(key):
      return googlemaps.Client(key=key)


  def __init__(self, gmapsKey):
    """
      Initialises a new instance of the Travel class
      which can be used for finding travel information
      from one place to another using the Google Maps API.

      @param gmapsKey:(string) The Google Maps API key.
    """
    self._gmapsKey = gmapsKey
    self._gmapsClient = self.GmapsFactory.newGmapsClient(key=self._gmapsKey)


  def find(self, orig, dest, metric, mode="walking", measure="value"):
    """
      Method to find some travel information about two different locations.

      @param orig:(See googlemaps.distance_matrix for correct type)
        The coordinates of the origin location.

      @param dest:(See googlemaps.distance_matrix for correct type)
        The coordinates of the destination location.

      @param metric:(string) Specify the metric in relation to the two
        locations, currently supported is 'distance', 'duration'.

      @param mode:(string) The mode of travel.

      @param measure:(string) Whether to return a text based measure or a correct
        measure according to the value. E.g text=4.32km, value=4.25
    """
    # Send request.
    response = GmapsResponse(self._gmapsClient.distance_matrix(orig, dest, mode=mode))
    return response.matrixInfo(metric, measure)
