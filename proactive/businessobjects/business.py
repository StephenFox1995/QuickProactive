from datetime import datetime

class Period(object):
  def __init__(self, begin, end):
    if isinstance(begin, datetime) and isinstance(end, datetime):
      self.begin = begin
      self.end = end
    else:
      raise TypeError(
        "begin and end type should be type<'datetime> not %s %s" % (type(begin), type(end))
      )

  @staticmethod
  def floatsToDatetimes(begin, end):
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
    return (begin, end)



class Business(object):
  def __init__(self, businessID, name, address, contactNumber, coordinates, period):
    self._id = businessID
    self._name = name
    self._address = address
    self._contactNumber = contactNumber
    self._coordinates = coordinates
    if isinstance(period["begin"], float) or isinstance(period["end"], float):
      (begin, end) = Period.floatsToDatetimes(period["begin"], period["end"])
      self._period = Period(begin, end)
    else:
      raise TypeError(
        "period begin and end attributes should be type<'float'>"
      )

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
