# -*- coding: utf-8 -*-
import sys
from inputCheck import InitialDataHandler
from fileDump import FileDump

idh = InitialDataHandler(sys.argv)

students = idh.getStudents()
rooms = idh.getRooms()
outputFormat = idh.getOutputFormat()

for i in rooms:
    i["students"] = [{"id":x["id"], "name":x["name"]} for x in students if x["room"] == i["id"]]
    
fd = FileDump(outputFormat)
fd.writeFile("output", rooms)

print("all done")