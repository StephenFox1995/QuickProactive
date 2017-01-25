import unittest2
import sys
from datetime import datetime, timedelta

sys.path.append("../")
from priority import Order

class OrderTest(unittest2.TestCase):

  def setUp(self):
    self.deadline = 300 # 5 mins
    self.processing = 210 # 3.5 mins.
    self.profit = 20

  def test_timeLeftToProcess(self):
    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )
    expectedResult = self.deadline - self.processing
    self.assertEqual(expectedResult, order._timeLeftToProcess(self.deadline, self.processing))
  

  def test_addSeconds(self):
    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )
    baseTime = datetime(
      year=2017, 
      month=1, 
      day=1, hour=0, 
      minute=0, 
      second=0
    )
    expectedTime = datetime(
      year=2017, 
      month=1, 
      day=1, 
      hour=0, 
      minute=5
    )
    
    secondsToAdd = 300
    newTime = order._addSeconds(baseTime, secondsToAdd)
    self.assertEqual(newTime, expectedTime)
  

  def test_releaseAtNoBuffPeriod(self):
    deadline = 600 # 10 mins
    processing = 300 # 5 mins
    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )
    
    # Expected release time is 5 mins from now.
    expectedReleaseAtTime = (datetime.now() + timedelta(seconds=deadline) - timedelta(seconds=processing)).isoformat()
    releaseAtTime = order._releaseAt(deadline, processing).isoformat()

    # Compare them as string, with no seconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)

    
  def test_releaseAtWithBuffPeriod(self):
    deadline = 600 # 10 mins
    processing = 300 # 5 mins
    buff = 120 # 2 mins

    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )

    # Expected release time is 5 mins from now.
    expectedReleaseAtTime = \
      ( datetime.now() + 
        timedelta(seconds=deadline) - 
        timedelta(seconds=processing) - 
        timedelta(seconds=buff)
      ).isoformat()

    releaseAtTime = order._releaseAt(deadline, processing, buff=buff).isoformat()

    # Compare them as string, with no seconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)

  def test_releaseAtImmediateDeadline(self):
    deadline = 0 # 0 mins
    processing = 300 # 5 mins

    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )

    # Expected release time is now.
    expectedReleaseAtTime = datetime.now().isoformat()

    releaseAtTime = order._releaseAt(deadline, processing).isoformat()

    # Compare them as string, with no seconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)

  def test_releaseAtImmediateDeadlineWithBuffPeriod(self):
    deadline = 0 # 0 mins
    processing = 300 # 5 mins
    buff = 120 # 2 mins

    order = Order(
      id=1, 
      deadline=self.deadline, 
      profit=self.profit, 
      processing=self.processing
    )

    # Expected release time is now.
    expectedReleaseAtTime = datetime.now().isoformat()

    releaseAtTime = order._releaseAt(deadline, processing, buff=buff).isoformat()

    # Compare them as string, with no seconds.
    expectedReleaseAtTime = expectedReleaseAtTime[:-7]
    releaseAtTime = releaseAtTime[:-7]
    self.assertEqual(expectedReleaseAtTime, releaseAtTime)

    

if __name__ == "__main__":
  unittest2.main()