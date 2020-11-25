# -*- coding: utf-8 -*-
import sys
from input_check import InitialDataHandler
from file_dump import FileDump

initial_data_handler = InitialDataHandler(sys.argv)

students = initial_data_handler.getStudents()
rooms = initial_data_handler.getRooms()
outputFormat = initial_data_handler.getOutputFormat()

for room in rooms:
	students_in_room = []
	for student in students:
		if student["room"] == room["id"]:
			students_in_room.append({"id":student["id"], "name":student["name"]})
	room["students"] = students_in_room
    
file_dump = FileDump(outputFormat)
file_dump.writeFile("output", rooms)

print("all done")