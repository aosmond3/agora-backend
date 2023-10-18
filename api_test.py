import logging
import subprocess

from . import data_accessor as da


DB_NAME = "test.sqlite"

def test_foreign_key():
    da.initialize_db(db_name=DB_NAME)
    da.create_user(1, "aosmond", "password")
    da.create_group(1, "Boone & Sons", 1)
    try:
        da.create_group(5, "Boone & Sons", 13)
    except:
        print("oh well, moving on")
    da.create_user(2, "josmond", "password")
    da.create_group(2, "brothers", 2)

    response = da.get_users()
    print(response)


def main() -> None:
    subprocess.run(["rm", DB_NAME])
    logging.basicConfig(level=logging.INFO)

    test_foreign_key()


if __name__=="__main__":
    main()