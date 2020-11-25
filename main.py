import sys
import argparse
from input_check import InputHandler
from file_dump import FileDump

def main():
	parser = argparse.ArgumentParser(description="Join students and rooms files")
	parser.add_argument("-s", "--students", default="students.json", help="Path to students file")
	parser.add_argument("-r", "--rooms", default="rooms.json", help="Path to rooms file")
	parser.add_argument("-o", "--output", help="Type of an output file")
	args = parser.parse_args()
	join(args)

def join(args):
	input_handler = InputHandler()	
	students = input_handler.getData("students", args.students)
	rooms = input_handler.getData("rooms", args.rooms)
	output = input_handler.getOutput(args.output)

	for room in rooms:
		students_in_room = []
		for student in students:
			if student["room"] == room["id"]:
				students_in_room.append({"id":student["id"], "name":student["name"]})
		room["students"] = students_in_room
	    
	file_dump = FileDump(output)
	file_dump.write_to_file(rooms)

if __name__ == "__main__":
	main()
	print("all done!")