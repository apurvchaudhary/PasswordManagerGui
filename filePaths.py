import os

FILE_NAME = "passwords.csv"
DIR_NAME = "SecurePassManager/"
DIR_PATH = os.path.expanduser('~/Documents/')
PASSWORD_CSV_PATH = DIR_PATH + DIR_NAME + FILE_NAME


def set_file_paths():
    if not os.path.exists(DIR_PATH + DIR_NAME):
        os.mkdir(DIR_PATH + DIR_NAME)
    if not os.path.exists(PASSWORD_CSV_PATH):
        with open(PASSWORD_CSV_PATH, "a"):
            pass
