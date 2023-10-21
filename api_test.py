import logging
import subprocess

import data_accessor as da


DB_NAME = "test.sqlite"

def test_foreign_key():
    da.initialize_db()
    da.create_user("aosmond", "password")
    da.create_group(1, "Boone & Sons", "aosmond", "gpass")
    try:
        da.create_group(5, "Boone & Sons", "notPerson", "passy")
    except:
        print("oh well, moving on")
    da.create_user("josmond", "password")
    da.create_group(2, "brothers", "josmond", "pass5")

    response = da.get_users()
    print(response)

def test_join_group(username: str, group_id: int, group_password: str):
    da.initialize_db()
    da.create_user(username, "aosmond_password")
    da.create_group(group_id, "Boone & Sons", username, group_password)

    try:
        print(da.join_group(username, group_id, group_password))
    except:
        print("yay this failed b/c user added to group when they create it!!!")

    da.create_user("cam", "lololpass")
    da.join_group("cam", group_id, group_password)

def test_get_groups_for_user(username: str):
    da.initialize_db()
    da.create_user(username, "aosmond_password")
    da.create_group(1, "Boone & Sons", username, "b&spass")
    da.create_group(2, "Brothers", username, "bros")
    print(da.get_groups_for_user(username))

def main() -> None:
    subprocess.run(["rm", DB_NAME])
    logging.basicConfig(level=logging.WARNING)

    # test_foreign_key()
    # test_join_group("aosmond", 1, "b&spass")
    test_get_groups_for_user("aosmond")


if __name__=="__main__":
    main()