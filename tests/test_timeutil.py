from datetime import datetime, timedelta
from proactive.utils import timeutil
from unittest2 import TestCase


class TestTimeutil(TestCase):
  def test_addSeconds(self):
    seconds = 300 # 5 mins
    baseTime = datetime.now()
    expectedTime = baseTime + timedelta(seconds=seconds)
    self.assertEqual(timeutil.addSeconds(baseTime, seconds), expectedTime)
