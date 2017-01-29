from unittest import TestCase
from proactive.travel import Travel, Metric
from mock import patch

gmapsResponse = {
  "status": "OK",
  "rows": [{
    "elements": [{
      "duration": {
        "text": "5 mins",
        "value": 307
      },
      "distance": {
        "text": "0.4 km",
        "value": 400
      },
      "status": "OK"
    }]
  }],
  "origin_addresses": [
    "The Warehouse, Coke Ln, Smithfield, Dublin 7, Ireland"
  ],
  "destination_addresses": [
    "Usher's Court, Usher's Quay, Merchants Quay, Dublin 8, Ireland"
  ]
}

class GoogleMapsClient(object):
  def __init__(self):
    pass

  def distance_matrix(self, orig, dest, mode=None):
    # Mock result from the gmaps distance matrix.
    return gmapsResponse


class TestTravel(TestCase):

  @patch('proactive.travel.Travel.GmapsFactory')
  def test_findWithValueMetric(self, GmapsFactoryMock):
    gmapsKey = "mockKey1234" # key not needed as GmapsClient will be mocked.
    GmapsFactoryMock.newGmapsClient.return_value = GoogleMapsClient()

    businessCoordinates = {"lat": 53.345376, "lng": -6.279931}
    customerCoordinates = {"lat": 53.345466, "lng": -6.278987}

    travel = Travel(gmapsKey)
    arrivalTime = travel.find(
      businessCoordinates,
      customerCoordinates,
      Metric.DURATION,
      measure="value"
    )
    self.assertEqual(arrivalTime, gmapsResponse["rows"][0]["elements"][0]["duration"]["value"])

