from unittest import TestCase
from datetime import datetime
from proactive.priority.business import Period, Business


class TestPeriod(TestCase):
  def test_transformStringToPeriod(self):
    begin = 9.00
    end = 21.00
    (beginResult, endResult) = Period.floatsToDatetimes(begin, end)

    beginStr = str(begin).split(".")
    endStr = str(end).split(".")
    beginHour = float(beginStr[0])
    beginMinute = float(beginStr[1])
    endHour = float(endStr[0])
    endMinute = float(endStr[1])
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    begin = datetime(year, month, day, int(beginHour), int(beginMinute))
    end = datetime(year, month, day, int(endHour), int(endMinute))
    self.assertEqual(beginResult, begin)
    self.assertEqual(endResult, end)



class TestBusiness(TestCase):
  def test_init(self):
    businessID = "test1234"
    name = "TestBusiness"
    address = "Test Address"
    contactNumber = "3974392"
    coordinates = {"lat": -22, "long": 22}
    period = {"begin": 9.00, "end": 21.00}

    business = Business(
      businessID=businessID,
      name=name,
      address=address,
      contactNumber=contactNumber,
      coordinates=coordinates,
      period=period
    )
    _period = Period.floatsToDatetimes(period["begin"], period["end"])
    expectedPeriod = Period(_period[0], _period[1])
    self.assertEqual(business.businessID, businessID)
    self.assertEqual(business.name, name)
    self.assertEqual(business.address, address)
    self.assertEqual(business.contactNumber, contactNumber)
    self.assertEqual(business.coordinates, coordinates)
    self.assertEqual(business.period.begin, expectedPeriod.begin)
    self.assertEqual(business.period.end, expectedPeriod.end)
