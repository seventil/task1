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


def index_tables(table_name, column_to_index, connection: DBConnection):
    conn = connection.get_conn()
    cursor = conn.cursor()
    if table_exists(table_name, connection):
        cursor.execute(f"ALTER TABLE {table_name} ADD INDEX ({column_to_index})")
    

def table_exists(table_name, connection: DBConnection):
    conn = connection.get_conn()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for row in cursor:
        try:
            if row[0] == table_name:
                return True
        except Exception:
            return False
    return False


class QueryOrganizer():
    def __init__(self, query_number):
        self.number = query_number
        self.queries = {}
        self.queries[1] = ("SELECT r.id, r.name, s.cnt FROM rooms r "
                           "JOIN (SELECT COUNT(students.id) cnt, room "
                           "FROM students GROUP BY room) s ON (r.id = s.room)")
        self.queries[2] = ("SELECT r.id, r.name, brd.avr FROM rooms r "
                           "JOIN (SELECT CAST(AVG(students.birthday) AS CHAR) avr, room "
                           "FROM students GROUP BY room ORDER BY avr "
                           "DESC LIMIT 5) brd ON (r.id = brd.room)")
        self.queries[3] = ("SELECT r.id, r.name, df.d FROM rooms r "
                           "JOIN (SELECT DATEDIFF(MAX(birthday), MIN(birthday)) d, room "
                           "FROM students GROUP BY room ORDER BY d "
                           "DESC LIMIT 5) df ON (r.id = df.room)")
        self.queries[4] = ("SELECT m.room FROM "
                           "(SELECT room FROM students WHERE sex IN ('F') GROUP BY room) f "
                           "JOIN (SELECT room FROM students "
                           "WHERE sex in ('M') GROUP BY room) m "
                           "ON (f.room = m.room)")
        
        self.column_names = {}
        self.column_names[1] = ('room_id', 'room_name', 'students_count')
        self.column_names[2] = ('room_id', 'room_name', 'average_bd')
        self.column_names[3] = ('room_id', 'room_name', 'date_diff')
        self.column_names[4] = ('room_id',)

    def get_query(self):
        return self.queries[self.number]

    def get_column_names(self):
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
    create_tables(db_connection, cleanse=True)

    insert_json_into_db(json_data, "rooms", db_connection)
    insert_json_into_db(json_data2, "students", db_connection)

    a = get_json_from_query(QueryOrganizer(4), db_connection)
    for i in range(5):
        print(a[i])

    index_tables("students", "birthday", db_connection)


