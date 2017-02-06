from datetime import timedelta, datetime

def releaseAt(deadline, processing):
  """
  The release time is calculate in the following way:

  r = deadline - processing

  where:
    deadline:   is the time the order should be processed by.
    processing: the time it will take to process the order.

  @param deadline:(datetime.datetime) The deadline.

  @param processing:(int) The amount of time in seconds the item will take to process.
  """
  if isinstance(deadline, datetime):
    return deadline - timedelta(seconds=processing)
  else:
    raise TypeError("Deadline must be of type <type 'datetime'>, not %s" % type(deadline))
