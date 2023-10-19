import logging
import subprocess

import data_accessor as da


DB_NAME = "test.sqlite"

def test_foreign_key():
    da.initialize_db()
    da.create_user(1, "aosmond", "password")
    da.create_group(1, "Boone & Sons", 1, "gpass")
    try:
        da.create_group(5, "Boone & Sons", 13, "passy")
    except:
        print("oh well, moving on")
    da.create_user(2, "josmond", "password")
    da.create_group(2, "brothers", 2, "pass5")

    response = da.get_users()
    print(response)

def test_join_group(user_uuid: int, group_id: int, group_password: str):
    da.initialize_db()
    da.create_user(1, "aosmond", "aosmond_password")
    da.create_group(1, "Boone & Sons", 1, "b&spass")

    print(da.join_group(user_uuid, group_id, group_password))

def test_get_groups_for_user(user_uuid: int):
    da.initialize_db()
    da.create_user(1, "aosmond", "aosmond_password")
    da.create_user(2, "guunt", "guuntymanpass")
    da.create_group(1, "Boone & Sons", 1, "b&spass")
    da.create_group(2, "Brothers", 1, "bros")
    da.join_group(2, 1, "b&spass")
    print(da.get_groups_for_user(2))

def main() -> None:
    subprocess.run(["rm", DB_NAME])
    logging.basicConfig(level=logging.WARNING)

    # test_foreign_key()
    # test_join_group(1, 1, "b&spass")
    test_get_groups_for_user(1)


if __name__=="__main__":
    main()