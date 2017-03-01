from proactive.priority.taskunit import TaskUnit
from .testutil import tHour

"""
  Visually the tasks would look something like this:

              t1 ----
                t2 -----------------------
                                                        t3 -----            t7------------
                                                          t4 ----       t6 --------------
                                                            t5 ---------------
                                                                                     t8------------       t9------------
    9.00-----9.30-----|10.00-----10.30-----|11.00-----11.30-----|12.00-----12.30-----|13.00-----13.30-----|14.00-----14.30-----|15.00-----15.30-----|16.00-----16.30
"""
testtaskset = [
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(10, 00),
    profit=0,
    processing=0,
    release=tHour(9, 30),
    taskID="t1"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(11, 00),
    profit=0,
    processing=0,
    release=tHour(9, 40),
    taskID="t2"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(12, 00),
    profit=0,
    processing=0,
    release=tHour(11, 30),
    taskID="t3"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(12, 00),
    profit=0,
    processing=0,
    release=tHour(11, 35),
    taskID="t4"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(12, 30),
    profit=0,
    release=tHour(11, 50),
    processing=0,
    taskID="t5"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(13, 15),
    profit=0,
    processing=0,
    release=tHour(12, 15),
    taskID="t6"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(13, 20),
    profit=0,
    processing=0,
    release=tHour(12, 30),
    taskID="t7"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(13, 30),
    profit=0,
    processing=0,
    release=tHour(13, 00),
    taskID="t8"
  ),
  TaskUnit(
    createdAt=tHour(0, 0),
    deadline=tHour(14, 30),
    profit=0,
    processing=0,
    release=tHour(14, 00),
    taskID="t9"
  )
]