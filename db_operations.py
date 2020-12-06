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


def create_tables(connection: DBConnection):
    conn = connection.get_conn()
    cursor = conn.cursor()

    TABLES = {}
    TABLES["rooms"] = (
        "CREATE TABLE IF NOT EXISTS `rooms` ("
        "`id` INT UNSIGNED NOT NULL,"
        "`name` VARCHAR(30) NOT NULL,"
        "PRIMARY KEY (`id`))")
    TABLES["students"] = (
        "CREATE TABLE IF NOT EXISTS `students` ("
        "`id` INT UNSIGNED NOT NULL,"
        "`name` VARCHAR(30) NOT NULL,"
        "`birthday` DATE,"
        "`sex` CHAR,"
        "`room` INT UNSIGNED NOT NULL,"
        "PRIMARY KEY (`id`),"
        "FOREIGN KEY (`room`) REFERENCES `rooms` (`id`) ON DELETE CASCADE)")
    for table_name in TABLES:
        cursor.execute(TABLES[table_name])
    cursor.close()
    conn.close()


def insert_students(connection: DBConnection, data):
    cursor = connection.cursor

def insert_rooms(connection: DBConnection, data):
    cursor = connection.cursor
    cursor.execute()


def get_joined(connection: DBConnection):
    cursor = connection.cursor
    cursor.execute()
