from datetime import datetime, timedelta

def releaseAt(deadline, processing, created=datetime.now()):
  """
  The release time is calculate in the following way:

  r = deadline - processing

  where:
    deadline:   is the time the order should be processed by.
    processing: the time it will take to process the order.

  @param deadline:(int) The deadline in seconds, so the latest the item needs to be ready by.

  @param processing:(int) The amount of time in seconds the item will take to process.

  @param created:(datetime.datetime) The time the item was 'spawned' or came into existence.

  """
  _deadline = created + timedelta(seconds=deadline)
  _processing = timedelta(seconds=processing)
  return _deadline - _processing

  # # if the calculation somehow
  # # underflows to a time before the order
  # # the release time should be set to the current time.
  # if release < created:
  #   return datetime.now()
  # return release



