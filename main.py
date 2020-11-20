# -*- coding: utf-8 -*-
import sys
from inputCheck import InitialDataHandler

#args = ["1","students.json","rooms.json","XML"]

idh = InitialDataHandler(sys.argv)
students = idh.getStudents()
rooms = idh.getRooms()
outputFormat = idh.getOutputFormat()


print("outputFormat = ", outputFormat)
print("rooms ", len(rooms))
print("students ", len(students))
print("finished")
   