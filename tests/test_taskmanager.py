from unittest import TestCase
from intervaltree import IntervalTree
from proactive.priority.taskmanager import TaskManager

class TestTaskManager(TestCase):

  def test_numberOfConflicts(self):
    tasks = [
      {"id": "t1", "release": 9.30, "deadline": 10.00, "status": "unassigned"},
      {"id": "t2", "release": 9.40, "deadline": 11.00, "status": "unassigned"},
      {"id": "t3", "release": 11.30, "deadline": 12.00, "status": "unassigned"},
      {"id": "t4", "release": 11.35, "deadline": 12.00, "status": "unassigned"},
      {"id": "t5", "release": 11.50, "deadline": 12.30, "status": "unassigned"}
    ]
    taskManager = TaskManager(period=(8, 9))
    taskManager.addTasks(tasks)
    conflicts = taskManager.findConflicts().allGreaterThan(2)
    self.assertEqual(len(conflicts), 1)


