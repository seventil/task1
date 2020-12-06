import input_handle
from data_dump import DataDumper, WriterFactory
import db_operations as dbo


def main():

    # students.json rooms.json JSON
    args = input_handle.get_initial_args()
    students = input_handle.get_data_from_file(args.students)
    rooms = input_handle.get_data_from_file(args.rooms)

    db_connection = dbo.DBConnection("localhost", "root", "root", "task4")
    dbo.create_tables(db_connection, cleanse=True)

    dbo.insert_json_into_db(rooms, "rooms", db_connection)
    dbo.insert_json_into_db(students, "students", db_connection)

    solved_problems_results = {
        'first_problem': dbo.get_json_from_query(dbo.QueryOrganizer(1), db_connection)


    }

    dumper = DataDumper(WriterFactory())
    for name, data in solved_problems_results:
        dumper.dump_data(data, args.output, name)


    


if __name__ == "__main__":
    main()
