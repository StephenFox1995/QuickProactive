import googlemaps


class Metric(object):
  DURATION = "duration"
  DISTANCE = "distance"


class GmapsResponse(object):
  """
    Encapusulates a response from the Google Maps API, specifically the Distance Matrix API.
    Exposes common methods which may be useful for extracting information from the response.
  """
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
      raise ValueError("Uknown metric: %s" % metric)


class Travel(object):
  class GmapsFactory(object):
    @staticmethod
    def newGmapsClient(key):
      return googlemaps.Client(key=key)

  #Keep cache of previous reponses, as to reduce requests on Google Maps API (free version)
  # TODO: There has to be a better way of doing this.
  __responseCache = {}


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
    coords = "%s,%s" % (orig, dest) # used as key for cache.
    # Send request.
    try:
      response = self.__responseCache[coords]
    except KeyError:
      response = GmapsResponse(self._gmapsClient.distance_matrix(orig, dest, mode=mode))
      self.__responseCache[coords] = response

    return response.matrixInfo(metric, measure)
