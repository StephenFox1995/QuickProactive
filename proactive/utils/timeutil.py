from datetime import datetime, timedelta

def addSeconds(time, seconds):
  """
  Adds n seconds to the time arg.
  """
  return time + timedelta(seconds=seconds)


def tHour(hour, minute):
  year = datetime.now().year
  month = datetime.now().month
  day = datetime.now().day
  return datetime(year, month, day, hour, minute, 0, 0)
