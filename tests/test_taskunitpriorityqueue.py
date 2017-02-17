from unittest import TestCase
from proactive.priority.taskunitpriorityqueue import TaskUnitPriorityQueue
from proactive.priority.taskunit import TaskUnit


class TestTaskUnitPriorityQueue(TestCase):
  def setUp(self):
    from datetime import datetime
    self._createdAt = datetime.now()
    self._deadline = 600 # 10 mins
    self._profit = 2.00
    self._processing = 300
    self._taskID = "test1"


  def test_count(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing,
        taskID=self._taskID
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)


  def test_pushToEmptyQueue(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing,
        taskID=self._taskID
      )
    ]
    pQueue = TaskUnitPriorityQueue()
    pQueue.push(items)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)

  def test_pushToPopulatedQueue(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing,
        taskID=self._taskID
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    pQueue.push(
      TaskUnit(
        createdAt=self._createdAt,
        deadline=100,
        profit=200,
        processing=20,
        taskID=self._taskID
      )
    )
    expectedCount = 2
    self.assertEqual(pQueue.count(), expectedCount)

  def test_pushWithNonListObject(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing,
      taskID=self._taskID
    )
    pQueue = TaskUnitPriorityQueue()
    pQueue.push(item)
    expectedCount = 1
    self.assertEqual(pQueue.count(), expectedCount)

  def test_pushWithListObject(self):
    items = [
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing,
        taskID=self._taskID
      ),
      TaskUnit(
        createdAt=self._createdAt,
        deadline=self._deadline,
        profit=self._profit,
        processing=self._processing,
        taskID=self._taskID
      )
    ]
    pQueue = TaskUnitPriorityQueue()
    pQueue.push(items)
    self.assertEqual(pQueue.count(), 2)

  def test_constructWithNonListObject(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing,
      taskID=self._taskID
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
        processing=processing,
        taskID=self._taskID
      ),
      TaskUnit(
        createdAt=self._createdAt,
        deadline=deadline2,
        profit=self._profit,
        processing=processing,
        taskID='test2'
      )
    ]
    pQueue = TaskUnitPriorityQueue(items)
    expectedFirstPop = items[1]
    expectedSecondPop = items[0]
    self.assertEqual(pQueue.pop(), expectedFirstPop)
    self.assertEqual(pQueue.pop(), expectedSecondPop)

  def test_remove(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing,
      taskID=self._taskID
    )
    pQueue = TaskUnitPriorityQueue()
    pQueue.push(item)
    pQueue.remove(item.taskID)
    self.assertEqual(pQueue.count(), 0)

  def test_contains(self):
    item = TaskUnit(
      createdAt=self._createdAt,
      deadline=self._deadline,
      profit=self._profit,
      processing=self._processing,
      taskID=self._taskID
    )
    pQueue = TaskUnitPriorityQueue()
    # test contains with push pop
    pQueue.push(item)
    self.assertTrue(pQueue.contains(item.taskID))
    pQueue.pop()
    self.assertFalse(pQueue.contains(item.taskID))
    # test contains with push remove
    pQueue.push(item)
    self.assertTrue(pQueue.contains(item.taskID))
    pQueue.remove(item.taskID)
    self.assertFalse(pQueue.contains(item.taskID))
