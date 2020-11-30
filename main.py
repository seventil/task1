import sys
import input_check
from data_dump import DataDumper, WriterFactory


def main():
    try:
        args = input_check.get_initial_args()
        students = input_check.get_data_from_file(args.students)
        rooms = input_check.get_data_from_file(args.rooms)

        for room in rooms:
            students_in_room = []
            for student in students:
                if student["room"] == room["id"]:
                    students_in_room.append({"id": student["id"],
                                             "name": student["name"]})
            room["students"] = students_in_room

        dumper = DataDumper(WriterFactory())
        dumper.dump_data(rooms, args.output, "output")

    except Exception:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
