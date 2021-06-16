import os

# file paths related to project
CSV_FILE_NAME = "passwords.csv"
DIR_NAME = "SecurePassManager/"
DIR_PATH = os.path.expanduser('~/Documents/')
PASSWORD_CSV_PATH = DIR_PATH + DIR_NAME + CSV_FILE_NAME
HEX_DIGEST_FILE_PATH = DIR_PATH + DIR_NAME + "hexDigest.lock"


def set_file_paths():
    """
    automate dir & file paths settings & creations
    """
    if not os.path.exists(DIR_PATH + DIR_NAME):
        os.mkdir(DIR_PATH + DIR_NAME)
    if not os.path.exists(PASSWORD_CSV_PATH):
        with open(PASSWORD_CSV_PATH, "a"):
            pass
    if not os.path.exists(HEX_DIGEST_FILE_PATH):
        with open(HEX_DIGEST_FILE_PATH, "a") as hash_file:
            hash_file.write("03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4")
