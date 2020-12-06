import mysql.connector


class DBConnection():
    def __init__(self, db_host, db_user, db_passwd, db_name):
        self.host = db_host
        self.user = db_user
        self.passwd = db_passwd
        self.name = db_name
        self.conn = None

        checkdb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd
            )
        cursor = checkdb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.name}")
        checkdb.close()

    def get_conn(self):
        if self.conn is None:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.name
                )
        return self.conn


def create_tables(connection: DBConnection, cleanse=False):
    # создает новые таблицы, или удаляет все данные из уже созданных
    conn = connection.get_conn()
    cursor = conn.cursor()

    TABLES = {}
    TABLES["rooms"] = (
        "CREATE TABLE IF NOT EXISTS rooms ("
        "id INT UNSIGNED NOT NULL,"
        "name VARCHAR(30) NOT NULL,"
        "PRIMARY KEY (id))")
    TABLES["students"] = (
        "CREATE TABLE IF NOT EXISTS students ("
        "id INT UNSIGNED NOT NULL,"
        "name VARCHAR(30) NOT NULL,"
        "birthday DATE,"
        "sex CHAR,"
        "room INT UNSIGNED NOT NULL,"
        "PRIMARY KEY (id),"
        "FOREIGN KEY (room) REFERENCES rooms (id) ON DELETE CASCADE)")
    for table_name in TABLES:
        cursor.execute(TABLES[table_name])
        if cleanse:
            cursor.execute("DELETE FROM " + table_name)
    conn.commit()


def insert_json_into_db(json_data, table_name, connection: DBConnection):
    # метод принимает только лист диктов в параметре json_data
    conn = connection.get_conn()
    cursor = conn.cursor()
    
    for json_dict in json_data:
        if type(json_dict) == dict:            
            column_names = "(" + ", ".join([key for key in json_dict.keys()]) + ")"
            values = ", ".join(["'" + str(value) + "'" for value in json_dict.values()])
            query = ("INSERT INTO " + table_name + " " 
                    + column_names
                    + " VALUES ("
                    + values
                    + ")")
        else:
            raise Exception("Wrong json data structure")

        try:
            cursor.execute(query)
        except mysql.connector.errors.IntegrityError:
            print("Duplicate querry found, insert failed")

    conn.commit()


class QueryOrganizer():
    def __init__(self, query_number):
        self.number = query_number
        self.queries = {}
        self.queries[1] = ("SELECT r.id, r.name, s.cnt FROM rooms r "
             "JOIN (SELECT COUNT(students.id) cnt, room "
             "FROM students GROUP BY room) s ON (r.id = s.room) LIMIT 3")
        
        self.column_names = {}
        self.column_names[1] = ('room_id', 'room_name', 'students_count')

    def get_query():
        return self.queries[self.number]

    def get_column_names():
        return self.column_names[self.number]


def get_json_from_query(query_org: QueryOrganizer, connection: DBConnection):
    query = query_org.get_query()
    column_names = query_org.get_column_names()

    conn = connection.get_conn()
    cursor = conn.cursor()
    cursor.execute(query)

    export_data = []
    for row in cursor:             
        export_data.append(dict(zip(column_names, row)))

    return export_data


if __name__ == "__main__":    
    import json

    with open("rooms.json") as file:
        json_data = json.loads(file.read())
    with open("students.json") as file:
        json_data2 = json.loads(file.read())

    db_connection = DBConnection("localhost", "root", "root", "task4")
    # create_tables(db_connection, cleanse=True)

    # insert_json_into_db(json_data, "rooms", db_connection)
    # insert_json_into_db(json_data2, "students", db_connection)

    get_students_number_in_rooms(db_connection)
