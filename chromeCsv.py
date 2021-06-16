from csv import reader
from tkinter import messagebox

from constants import SAVE_TYPE
from filePaths import PASSWORD_CSV_PATH
from salt_algo import EncryptionDecryption


def chrome_csv_reader(file_path):
    """
    chrome password csv parser
    """
    with open(file_path, "r") as f:
        csv_reader = list(reader(f, delimiter=','))[1:]
    if not csv_reader:
        return messagebox.showinfo("Chrome CSV parser", "File doesn't contain any data")
    answer = messagebox.askyesnocancel("Chrome CSV parser", "Yes :- Save in encrypted form\n"
                                                            "No :- Save in plain/text form\n"
                                                            "Cancel :- Do nothing\n\n"
                                                            "Note : Saving in plain/text isn't encrypting")
    existed = []
    if PASSWORD_CSV_PATH:
        try:
            with open(PASSWORD_CSV_PATH, "r") as file:
                existed_reader = list(reader(file, delimiter=','))
            existed = [row[0] for row in existed_reader]
        except FileNotFoundError:
            pass
    if answer:
        for row in csv_reader:
            if row[0] in existed:
                messagebox.showerror("Chrome CSV parser", f"App {row[0]} already exists")
                continue
            try:
                EncryptionDecryption().encrypt(app=row[0], username=row[2], password=row[3], url=row[1])
            except Exception as e:
                return messagebox.showerror("Chrome CSV parser", f"Corrupted data error is : {e}")
        return messagebox.showinfo("Chrome CSV parser", "Unique Passwords saved in encrypted form")
    elif answer is False:
        for row in csv_reader:
            if row[0] in existed:
                messagebox.showerror("Chrome CSV parser", f"App {row[0]} already exists")
                continue
            try:
                EncryptionDecryption().write_to_excel(app=row[0], username=row[2], password=row[3], url=row[1],
                                                      key=SAVE_TYPE["PLAIN"])
            except Exception as e:
                return messagebox.showerror("Chrome CSV parser", f"Corrupted data error is : {e}")
        return messagebox.showinfo("Chrome CSV parser", "Unique Passwords saved in Plain/Text form")
    return messagebox.showinfo("Chrome CSV parser", "No passwords parsed or saved")
