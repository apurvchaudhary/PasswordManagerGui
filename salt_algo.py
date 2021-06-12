import csv
import os
from tkinter import messagebox

from cryptography.fernet import Fernet

from constants import PASSCODE, SAVE_TYPE, FILE_PATH, FILE_EXIST


class EncryptionDecryption:
    """
    encryption decryption class
    """

    def encrypt(self, app, password):
        """
        method to encrypt given password for given app with generated key in csv
        :param app: str
        :param password: str
        :return: write_to_excel callable
        """
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encoded = fernet.encrypt(password.encode())
        return self.write_to_excel(app, key, encoded)

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
    def write_to_excel(app, key, password):
        """
        method to write data to csv rows
        writing to csv two types : one is encrypted form with key OR plain text with key as Plain Text
        :param key: encryption key
        :param app: str
        :param password: str
        :return: messagebox
        """
        with open(FILE_PATH, "a", newline='') as csvfile:
            fieldnames = ['AppLabel', 'Key', 'Password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not FILE_EXIST:
                writer.writeheader()
            if key == SAVE_TYPE["PLAIN"]:
                writer.writerow({"AppLabel": app, "Key": key, "Password": password})
            else:
                writer.writerow({"AppLabel": app, "Key": key.decode('utf-8'), "Password": password.decode('utf-8')})
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
        with open("password_manage.csv", newline='') as csvfile:
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
        if not os.path.exists(FILE_PATH):
            return messagebox.showerror("Password file error", "either password file deleted or empty")
        if not passcode == PASSCODE:
            return messagebox.showerror("wrong passcode", "Please provide correct passcode")
        with open(FILE_PATH, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == app_name:
                    if row[1] == SAVE_TYPE["PLAIN"]:
                        return messagebox.showinfo(f"{app_name}", f"Password is : {row[2]}")
                    key = bytes(row[1], 'utf-8')
                    encoded_pass = bytes(row[2], 'utf-8')
                    return messagebox.showinfo(
                        f"{app_name}", f"{app_name} Password : {self.decrypt(key=key, enc_password=encoded_pass)}")
