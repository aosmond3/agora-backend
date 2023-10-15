import sqlite3
import logging

DB_NAME = "test.db"


class SQLite():
    """
    Context manager class for handling connections to a sqlite DB.
    It automatically commits or rolls back open transactions when
    leaving the body of the context manager. It also calls the close()
    function of the cursor and connection objects when leaving the
    body of the context manager.
    """

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def __enter__(self) -> None:
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback) -> None:
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
        cursor.execute("begin") # need to manually start transaction because executing DDL statements

        query = """
        CREATE TABLE IF NOT EXISTS user
        (username TEXT PRIMARY KEY)
        """
        cursor.execute(query)


def create_users():
    usernames = [("Andrew",), ("Justin",), ("Cameron",)]
    with SQLite(db_name=DB_NAME) as cursor:
        cursor.executemany("INSERT INTO user VALUES(?)", usernames)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    initialize_db()
    create_users()


if __name__=="__main__":
    main()