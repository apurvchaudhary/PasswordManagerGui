import csv
import hashlib
import os
from tkinter import messagebox

from cryptography.fernet import Fernet

from constants import SAVE_TYPE
from filePaths import PASSWORD_CSV_PATH as FILE_PATH, HEX_DIGEST_FILE_PATH


class EncryptionDecryption:
    """
    encryption decryption class
    """

    def encrypt(self, app, username, password, url):
        """
        method to encrypt given password for given app with generated key in csv
        :param app: str
        :param password: str
        :return: write_to_excel callable
        """
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encoded = fernet.encrypt(password.encode())
        return self.write_to_excel(app=app, username=username, password=encoded, url=url, key=key)

    @staticmethod
    def decrypt(key, enc_password):
        """
        method to decrypt encrypted password with given key
        :param key: key for decryption
        :param enc_password: encrypted password
        :return: str
        """
        fernet = Fernet(key)
        return fernet.decrypt(enc_password).decode()

    @staticmethod
    def write_to_excel(app, username, password, url, key):
        """
        method to write data to csv rows
        writing to csv two types : one is encrypted form with key OR plain text with key as Plain Text
        """
        file_exist = os.path.exists(FILE_PATH)
        with open(FILE_PATH, "a", newline='') as csvfile:
            fieldnames = ['AppLabel', 'Username', 'Url', 'Password', 'Key']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exist:
                writer.writeheader()
            if key == SAVE_TYPE["PLAIN"]:
                writer.writerow({"AppLabel": app, "Username": username, "Url": url,
                                 "Password": password, "Key": key})
            else:
                writer.writerow({"AppLabel": app, "Username": username, "Url": url,
                                 "Password": password.decode('utf-8'), "Key": key.decode('utf-8')})
            return messagebox.showinfo("Success", f"Password for {app} saved successfully")

    @staticmethod
    def get_all_app_labels():
        """
        get all app names to show in dropdown for further seeing password
        :return: list
        """
        app_names = []
        if not os.path.exists(FILE_PATH):
            return app_names
        with open(FILE_PATH, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == "AppLabel":
                    continue
                app_names.append(row[0])
        return app_names

    def show_password(self, passcode, app_name):
        """
        method to show password after success of passcode for given app_name
        :param passcode: private key
        :param app_name: str
        :return: messagebox
        """
        hashed = hashlib.sha256(passcode.encode()).hexdigest()
        if not os.path.exists(FILE_PATH):
            return messagebox.showerror("Password file error", "either password csv file deleted or empty")
        with open(HEX_DIGEST_FILE_PATH, "r") as hex:
            read_hash = hex.read()
        if not hashed == read_hash:
            return messagebox.showerror("wrong passcode", "Please provide correct passcode")
        with open(FILE_PATH, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == app_name:
                    if row[4] == SAVE_TYPE["PLAIN"]:
                        _info = f"Name : {row[0]}\nUsername : {row[1]}\nUrl : {row[2]}\nPassword : {row[3]}"
                        return messagebox.showinfo(f"{app_name}", _info)
                    key, encoded_pass = bytes(row[4], 'utf-8'), bytes(row[3], 'utf-8')
                    password = self.decrypt(key=key, enc_password=encoded_pass)
                    _info = f"Name : {row[0]}\nUsername : {row[1]}\nUrl : {row[2]}\nPassword : {password}"
                    return messagebox.showinfo("Password data", _info)
