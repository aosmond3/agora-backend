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
        if exc_type:
            logging.warning(f"Rolling back due to exception: {exc_type}")
            logging.warning(f"exc_value: {exc_value}\ntraceback: {traceback}")
            self.connection.rollback()
        else:
            logging.info("Committing transaction")
            self.connection.commit()

        logging.info("Closing cursor & connection")
        self.cursor.close()
        self.connection.close()


def initialize_db(): # TODO: (long term) add creation datetime fields and such
    with SQLite(DB_NAME) as cursor:
        cursor.execute("begin") # start transaction (necessary so DDL statement CREATE TABLE doesn't autocommit)

        query = """
        CREATE TABLE IF NOT EXISTS "user" (
            "user_uuid"        INTEGER   PRIMARY KEY     NOT NULL,
            "username"    TEXT      UNIQUE          NOT NULL,
            "password"    TEXT                      NOT NULL
        );
        """
        cursor.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS "group" (
            "group_id"                  INTEGER     PRIMARY KEY     NOT NULL,
            "group_name"                TEXT                        NOT NULL,
            "group_admin_uuid"          INTEGER                     NOT NULL,
            "group_password"            TEXT                        NOT NULL,
            FOREIGN KEY("group_admin_uuid") REFERENCES "user"("user_uuid")
        );
        """
        cursor.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS "group_membership" (
            "user_uuid"     INTEGER     NOT NULL,
            "group_id"      INTEGER     NOT NULL,
            PRIMARY KEY("user_uuid", "group_id"),
            FOREIGN KEY("user_uuid") REFERENCES "user"("user_uuid"),
            FOREIGN KEY("group_id") REFERENCES "group"("group_id")
        );
        """
        cursor.execute(query)


def get_users() -> list[dict]:
    with SQLite(db_name=DB_NAME) as cursor:
        query = """
        SELECT "user_uuid", "username", "password"
        FROM "user";
        """
        cursor.execute(query)
        rows =  cursor.fetchall()

        if not rows: return rows
        # TODO: think about throwing exception instead so can be more specific about the error

        # construct response list
        users = []
        for row in rows:
            user = {}
            user["user_uuid"] = row["user_uuid"]
            user["username"] = row["username"]
            user["password"] = row["password"]
            users.append(user)

        return users


def get_groups_for_user(user_uuid: int):
    with SQLite(db_name=DB_NAME) as cursor:
        query = """
        SELECT "group_id"
        FROM "group_membership"
        WHERE "user_uuid" = :user_uuid
        """
        cursor.execute(query, {"user_uuid": user_uuid})
        rows = cursor.fetchall()

        if not rows: return rows # TODO: think about throwing exception instead so can be more specific about the error

        return {"group_ids": [row["group_id"] for row in rows]}


def get_group_password(group_id: int) -> dict:
    with SQLite(db_name=DB_NAME) as cursor:
        query = """
        SELECT "group_password"
        FROM "group"
        WHERE "group_id" = :group_id;
        """
        cursor.execute(query, {"group_id": group_id})
        row = cursor.fetchone()

        return {"group_password": row["group_password"]} if row else row
        # TODO: think about throwing exception instead so can be more specific about
        # the error in join_group()


def create_user(user_uuid: int, username: str, password: str):
    with SQLite(db_name=DB_NAME) as cursor:
        parameters = {
            "user_uuid": user_uuid,
            "username": username,
            "password": password
        }
        cursor.execute("""INSERT INTO "user" VALUES(:user_uuid, :username, :password)""", parameters)


def create_group(group_id: int, group_name: str, group_admin_uuid: int, group_password: str) -> None:
    """New group is created and user with uuid = to 'group_admin_uuid' is added to the group"""

    with SQLite(db_name=DB_NAME) as cursor:
        parameters = {
            "group_id": group_id,
            "group_name": group_name,
            "group_admin_uuid": group_admin_uuid,
            "group_password": group_password
        }
        cursor.execute("""INSERT INTO "group" VALUES(:group_id, :group_name, :group_admin_uuid, :group_password)""", parameters)

        parameters = {
            "user_uuid": group_admin_uuid,
            "group_id": group_id
        }
        cursor.execute("""INSERT INTO "group_membership" VALUES(:user_uuid, :group_id)""", parameters)


def join_group(user_uuid: int, group_id: int, group_password: str) -> bool:
    true_group_password = get_group_password(group_id)
    if not true_group_password or true_group_password["group_password"] != group_password:
        return False

    with SQLite(db_name=DB_NAME) as cursor:
        parameters = {
            "user_uuid": user_uuid,
            "group_id": group_id
        }
        cursor.execute("""INSERT INTO "group_membership" VALUES(:user_uuid, :group_id)""", parameters)
        return True