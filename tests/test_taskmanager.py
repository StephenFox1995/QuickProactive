from unittest import TestCase
from intervaltree import IntervalTree
from proactive.priority.taskmanager import TaskManager

class TestTaskManager(TestCase):
  def setUp(self):
   self._tasks = [
     {"id": "t1", "release": 9.30, "deadline": 10.00, "status": "unassigned"},
     {"id": "t2", "release": 9.40, "deadline": 11.00, "status": "unassigned"},
     {"id": "t3", "release": 11.30, "deadline": 12.00, "status": "unassigned"},
     {"id": "t4", "release": 11.35, "deadline": 12.00, "status": "unassigned"},
     {"id": "t5", "release": 11.50, "deadline": 12.30, "status": "unassigned"},
     {"id": "t6", "release": 14.50, "deadline": 15.30, "status": "unassigned"},
  ]


  def test_numberOfConflicts(self):
    taskManager = TaskManager(period=(8, 9))
    taskManager.addTasks(self._tasks)
    (underThreshold, overThreshold) = taskManager.findConflicts(threshold=2)
    print(underThreshold)
    print(overThreshold)
    self.assertEqual(len(underThreshold), 1)
    self.assertEqual(len(overThreshold), 1)
