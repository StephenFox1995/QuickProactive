from datetime import datetime, timedelta
import proactive.priority.release as release
from unittest2 import TestCase



class TestRelease(TestCase):
  def test_releaseAt(self):
    deadline = 300 # 5 mins
    processing = 60 # 1 min
    createdAt = datetime.now()

    # Expected release time is 4 mins from now.
    expectedReleaseAtTime = (
      createdAt + timedelta(seconds=deadline) -
      timedelta(seconds=processing)
    ).isoformat()
    releaseAtTime = release.releaseAt(deadline, processing, created=createdAt).isoformat()

    # Compare them as string, with no milliseconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)


  def test_releaseAtWithProcessingLargerThanDeadline(self):
    deadline = 300 # 5 mins
    processing = 360 # 6 min
    createdAt = datetime.now()

    expectedReleaseAtTime = (
      createdAt + timedelta(seconds=deadline) -
      timedelta(seconds=processing)
    ).isoformat()
    releaseAtTime = release.releaseAt(deadline, processing, created=createdAt).isoformat()

    # Compare them as string, with no milliseconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)
