import os

PASSCODE = 1234

SAVE_TYPE = {
    "PLAIN": "Plain Text",
    "ENCRYPIFY": "Encrypify"
}

FILE_PATH = "password_manage.csv"
FILE_EXIST = os.path.exists(FILE_PATH)
