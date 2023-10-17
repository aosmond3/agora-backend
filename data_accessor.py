import sqlite3
import logging

DB_NAME = "test.sqlite"


class SQLite():
    """
    Context manager class for handling connections to a sqlite DB.
    It automatically commits or rolls back open transactions when
    leaving the body of the context manager. It also calls the close()
    function of the cursor and connection objects when leaving the
    body of the context manager.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def __enter__(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON") # enforce foreign key constraints
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if (exc_type):
            logging.info(f"Rolling back due to exception: {exc_type}")
            self.connection.rollback()
        else:
            logging.info("Committing transaction")
            self.connection.commit()

        logging.info("Closing cursor & connection")
        self.cursor.close()
        self.connection.close()


def initialize_db():
    with SQLite(db_name=DB_NAME) as cursor:
        cursor.execute("begin") # start transaction (necessary so DDL statement CREATE TABLE doesn't autocommit)

        query = """
        CREATE TABLE IF NOT EXISTS "user" (
            "uuid"        INTEGER PRIMARY KEY NOT NULL,
            "username"    TEXT UNIQUE NOT NULL,
            "password"    TEXT NOT NULL
        );
        """
        cursor.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS "group" (
            "group_id"          INTEGER PRIMARY KEY NOT NULL,
            "group_name"        TEXT NOT NULL,
            "group_admin_uuid"  INTEGER NOT NULL,
            FOREIGN KEY("group_admin_uuid") REFERENCES "user"("uuid")
        );
        """
        cursor.execute(query)


def create_user(uuid: int, username: str, password: str):
    with SQLite(db_name=DB_NAME) as cursor:
        parameters = {
            "uuid": uuid,
            "username": username,
            "password": password
        }
        cursor.execute("""INSERT INTO "user" VALUES(:uuid, :username, :password)""", parameters)

def create_group(group_id: int, group_name: str, group_admin_uuid: int) -> None:
    with SQLite(db_name=DB_NAME) as cursor:
        parameters = {
            "group_id": group_id,
            "group_name": group_name,
            "group_admin_uuid": group_admin_uuid
        }
        cursor.execute("""INSERT INTO "group" VALUES(:group_id, :group_name, :group_admin_uuid)""", parameters)


def main() -> None:
    import subprocess

    subprocess.run(["rm", f"{DB_NAME}"])

    logging.basicConfig(level=logging.INFO)
    initialize_db()
    create_user(1, "aosmond", "password")
    create_group(1, "Boone & Sons", 1)
    try:
        create_group(5, "Boone & Sons", 13)
    except:
        print("oh well, moving on")
    create_user(2, "josmond", "password")
    create_group(2, "brothers", 2)


if __name__=="__main__":
    main()