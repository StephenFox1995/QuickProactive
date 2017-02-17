from datetime import datetime

class Period(object):
  def __init__(self, begin, end):
    if isinstance(begin, datetime) and isinstance(end, datetime):
      self.begin = begin
      self.end = end
    else:
      raise TypeError(
        "begin and end type should be %s not %s %s" % (datetime, type(begin), type(end))
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


  def __str__(self):
    return "%s - %s" % (self.begin, self.end)
