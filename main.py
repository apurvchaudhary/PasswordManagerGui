import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import simpledialog

from constants import SAVE_TYPE
from salt_algo import EncryptionDecryption


def show(var_show, window):
    """
    function to show password which user selects from drop down menu
    :param var_show: dropdown str
    :param window: tkinter obj
    :return: messagebox
    """
    app_name = var_show.get()
    if app_name:
        answer = int(
            simpledialog.askinteger("Passcode", "Enter your passcode", parent=window))
        if not answer:
            return messagebox.showerror("Empty passcode", "empty passcode not valid")
        obj = EncryptionDecryption()
        return obj.show_password(passcode=answer, app_name=app_name)
    return messagebox.showerror("App/Website/Software", "Empty app value not allowed")


def save_data(entry_field1, entry_field2, save_type, window):
    """
    save password to csv file in same directory as project
    :param entry_field1: entry widget
    :param entry_field2: entry widget
    :param save_type: option menu
    :param window: tkinter obj
    :return: messagebox/showdown func
    """
    app = entry_field1.get()
    password = entry_field2.get()
    save_type = save_type.get()
    if not app:
        return messagebox.showerror("App/Website/Software", "Empty Application value not allowed")
    if not password:
        return messagebox.showerror("Password", "Empty password not allowed")
    if save_type == SAVE_TYPE["PLAIN"]:
        EncryptionDecryption().write_to_excel(app=app, key=save_type, password=password)
        return show_down_menu(window)
    elif save_type == SAVE_TYPE["ENCRYPIFY"]:
        EncryptionDecryption().encrypt(app=app, password=password)
        return show_down_menu(window)
    else:
        return messagebox.showerror(title="Save Type", message="Choose at least one saving Mode type")


def show_down_menu(window):
    """
    show password menu comes only if csv exists in dir
    calling after saving new password too
    :param window: tkinter obj
    :return: show func
    """
    prompt3 = tk.Label(text="Check Saved Passwords Below", bg="#cc80ff", pady=2, font=("Times", "22", "bold italic"),
                       height=1, width=30)
    prompt3.grid(row=9, rowspan=1, pady=10)
    show_app_list = EncryptionDecryption.get_all_app_labels()
    if show_app_list:
        # option menu 1
        var_show = tk.StringVar(window)
        var_show.set("Saved")
        # second option menu
        option_show = tk.OptionMenu(window, var_show, *show_app_list)
        option_show.configure(width=10, font=("Times", "10", "bold"))
        option_show.grid(row=11, rowspan=1, stick="W", padx=20)
        # button
        button2 = tk.Button(text="Show Password", command=partial(show, var_show, window), font=("Times", "12", "bold"))
        button2.grid(row=13, rowspan=1, sticky="w", padx=20, pady=10)


class Password:
    """
    Password manager main class for initialising instance of tkinter library further using callables
    """

    def __init__(self):
        window = tk.Tk()
        # title
        window.title("PASSWORD MANAGER © 2021")
        # gui size
        window.geometry("500x450")
        window.configure(background='#00e6ac')
        # label
        prompt = tk.Label(text="By Apurv Chaudhary", bg="#cc80ff", pady=2,
                          font=("Times", "22", "bold italic"), height=1, width=30)
        prompt.grid(column=0, row=0)

        # entry field1
        prompt1 = tk.Label(text="Name of App/Website/Software", font=("Arial", "12", "bold"))
        prompt1.grid(row=1, rowspan=1, sticky="w", padx=20, pady=10)
        prompt1.configure(background='#00e6ac')
        entry_field1 = tk.Entry(width=30)
        entry_field1.grid(row=2, rowspan=1, sticky="w", padx=20)

        # ENTRY FIELD 2
        prompt2 = tk.Label(text="Password", font=("Arial", "12", "bold"))
        prompt2.grid(row=3, rowspan=1, sticky="w", padx=20, pady=10)
        prompt2.configure(background='#00e6ac')
        entry_field2 = tk.Entry(width=30)
        entry_field2.grid(row=4, rowspan=1, sticky="w", padx=20)

        # option menu 1
        var = tk.StringVar(window)
        var.set("Mode")
        option = tk.OptionMenu(window, var, "Plain Text", "Encrypify")
        option.configure(font=("Times", "10", "bold"))
        option.grid(row=5, rowspan=1, stick="W", padx=20, pady=10)

        # button
        button1 = tk.Button(text="Save Password",
                            command=partial(save_data, entry_field1, entry_field2, var, window),
                            font=("Times", "12", "bold"))
        button1.grid(row=7, rowspan=1, sticky="w", padx=20)

        show_down_menu(window)

        window.mainloop()


Password()
