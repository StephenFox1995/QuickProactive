from datetime import timedelta

def addSeconds(time, seconds):
  """
  Adds n seconds to the time arg.
  """
  return time + timedelta(seconds=seconds)
