from proactive.priority.taskunitpriorityqueue import TaskUnitPriorityQueue
from proactive.priority.taskunit import TaskUnit
from unittest2 import TestCase

class TestTaskUnitPriorityQueue(TestCase):
  def setUp(self):
    from datetime import datetime
    self._createdAt = datetime.now()
    self._deadline = 600 # 10 mins
    self._profit = 2.00
    self._processing = 300

  def test_count(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)

  def test_addToEmptyQueue(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing
      )
    ]
    pQueue = TaskUnitPriorityQueue()
    pQueue.add(items)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)

  def test_addToPopulatedQueue(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    pQueue.add(
      TaskUnit(
        createdAt=self._createdAt,
        deadline=100,
        profit=200,
        processing=20
      )
    )
    expectedCount = 2
    self.assertEqual(pQueue.count(), expectedCount)

  def test_addWithNonListObject(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing
    )
    pQueue = TaskUnitPriorityQueue()
    pQueue.add(item)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)

  def test_constructWithNonListObject(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing
    )
    with self.assertRaises(TypeError):
      _ = TaskUnitPriorityQueue(item)


  def test_popEmptyQueue(self):
    pQueue = TaskUnitPriorityQueue()
    with self.assertRaises(IndexError):
      pQueue.pop()

  def test_popOrderFromPopulatedQueueFromConstructor(self):
    # Use custom values here to ensure correct pop order.
    deadline1 = 500
    deadline2 = 200
    processing = 100

    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=deadline1,
        profit=self._profit,
        processing=processing
      ),
      TaskUnit(
        createdAt=self._createdAt,
        deadline=deadline2,
        profit=self._profit,
        processing=processing
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    expectedFirstPop = items[1]
    expectedSecondPop = items[0]
    self.assertEqual(pQueue.pop(), expectedFirstPop)
    self.assertEqual(pQueue.pop(), expectedSecondPop)



