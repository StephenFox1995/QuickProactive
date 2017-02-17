from datetime import datetime
from proactive.priority.period import Period


class Business(object):
  def __init__(self, businessID, name, address, contactNumber, coordinates, period):
    self._id = businessID
    self._name = name
    self._address = address
    self._contactNumber = contactNumber
    self._coordinates = coordinates
    period["begin"] = float(period["begin"])
    period["end"] = float(period["end"])
    (begin, end) = Period.floatsToDatetimes(period["begin"], period["end"])
    self._period = Period(begin, end)

  @property
  def businessID(self):
    return self._id

  @property
  def name(self):
    return self._name

  @property
  def address(self):
    return self._address

  @property
  def contactNumber(self):
    return self._contactNumber

  @property
  def coordinates(self):
    return self._coordinates

  @property
  def period(self):
    return self._period
