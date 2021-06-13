import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import simpledialog, filedialog

from constants import SAVE_TYPE, DISCLAIMER, TITLE_COLOR, SHOW_DOWN_TITLE_COLOR, GUI_BG_COLOR,\
    LABEL_COLOR, SHOW_DOWN_TITLE_BG_COLOR
from filePaths import set_file_paths
from salt_algo import EncryptionDecryption
from chromeCsv import chrome_csv_reader


def show(var_show, window):
    """
    function to show password which user selects from drop down menu
    :param var_show: dropdown str
    :param window: tkinter obj
    :return: messagebox
    """
    app_name = var_show.get()
    if app_name:
        answer = simpledialog.askstring("Passcode", "Enter your Passcode", show="*", parent=window)
        if answer is None:
            return
        elif answer == "":
            messagebox.showerror("Empty passcode", "Empty Passcode not valid")
            return show(var_show, window)
        obj = EncryptionDecryption()
        return obj.show_password(passcode=answer, app_name=app_name)
    return messagebox.showerror("App/Website/Software", "Empty app value not allowed")


def save_data(app, username, password, url, mode, window: tk):
    """
    save password to csv file in same directory as project
    """
    app = app.get()
    username = username.get()
    password = password.get()
    url = url.get()
    save_type = mode.get()
    if not app:
        return messagebox.showerror("App/Website/Software", "Empty Application value not allowed")
    if not username:
        return messagebox.showerror("Username", "Empty username not allowed")
    if not password:
        return messagebox.showerror("Password", "Empty password not allowed")
    if save_type == SAVE_TYPE["PLAIN"]:
        if not url:
            answer = messagebox.askyesno("URL confirmation", "Save without url ?")
            if not answer:
                return messagebox.showwarning(f"Url for app {app}", f"First add url for {app} then save!")
        EncryptionDecryption().write_to_excel(app=app, username=username, url=url, password=password, key=save_type)
        return show_down_menu(window)
    elif save_type == SAVE_TYPE["ENCRYPIFY"]:
        if not url:
            answer = messagebox.askyesno("URL confirmation", "Save without url ?")
            if not answer:
                return messagebox.showwarning(f"Url for app {app}", f"First add url for {app} then save!")
        EncryptionDecryption().encrypt(app=app, username=username, password=password, url=url)
        return show_down_menu(window)
    else:
        return messagebox.showerror(title="Save Type", message="Choose at least one saving Mode type")


def browse_file(window):
    """
    file browser for chrome password syncing
    """
    filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("CSV Files", "*.csv"),))
    label = tk.Label(window, text="")
    label.grid(column=1, row=14)
    label.configure(text=filename)
    if filename:
        chrome_csv_reader(filename)
    show_down_menu(window)


def show_down_menu(window):
    """
    show password menu comes only if csv exists in dir
    calling after saving new password too
    :param window: tkinter obj
    :return: show func
    """
    prompt4 = tk.Label(text="Select App & Click on Show Password", bg=SHOW_DOWN_TITLE_COLOR, pady=2, font=("Times", "20"),
                       height=1, width=30, fg=SHOW_DOWN_TITLE_BG_COLOR)
    prompt4.grid(row=7, pady=20, sticky="w", padx=20)
    show_app_list = EncryptionDecryption.get_all_app_labels()
    if show_app_list:
        # option menu 1
        var_show = tk.StringVar(window)
        var_show.set("Saved List")
        # second option menu
        option_show = tk.OptionMenu(window, var_show, *show_app_list)
        option_show.configure(width=20, font=("Times", "10", "bold"), bg="black", fg="white")
        option_show.grid(row=8, stick="w", padx=100)
        # button
        button2 = tk.Button(text="Show Password", command=partial(show, var_show, window), font=("Times", "12", "bold"),
                            bg=TITLE_COLOR, fg="black")
        button2.grid(row=8, sticky="e", padx=100)

    prompt5 = tk.Label(text="Sync Browser downloaded CSV File", bg=SHOW_DOWN_TITLE_COLOR, pady=2, font=("Times", "20"),
                       height=1, width=30, fg=SHOW_DOWN_TITLE_BG_COLOR)
    prompt5.grid(row=9, pady=20, sticky="w", padx=20)
    prompt_ = tk.Label(text="Browse csv file to sync", font=("Arial", "12"), fg=LABEL_COLOR)
    prompt_.grid(row=10, sticky="w", padx=120)
    prompt_.configure(background=GUI_BG_COLOR)
    button3 = tk.Button(window, text = "Browse",font=("Times", "12", "bold"),
                        command=partial(browse_file, window), bg="black", fg="white")
    button3.grid(row=10, sticky="e", padx=155)


def show_disclaimer():
    """
    func for showing disclaimer
    """
    return messagebox.showinfo("Disclaimer by Apurv Chaudhary", DISCLAIMER)


class Password:
    """
    Password manager main class for initialising instance of tkinter library further using callables
    """

    def __init__(self):
        set_file_paths()

        window = tk.Tk()
        # title
        window.title("PASSWORD MANAGER © 2021 www.apurvchaudhary.com")
        # gui size
        window.geometry("500x700")
        window.configure(background=GUI_BG_COLOR)
        # label
        prompt = tk.Label(text="128 bit Encrypted Password Manager", bg=TITLE_COLOR, pady=2,
                          font=("Times", "22", "bold"), height=1, width=30)
        prompt.grid(row=0, column=0)

        # ENTRY FIELD 1
        prompt1 = tk.Label(text="Name of App/Website/Software :", font=("Arial", "12"), fg=LABEL_COLOR)
        prompt1.grid(row=1, sticky="w", pady=20, padx=10)
        prompt1.configure(background=GUI_BG_COLOR)
        entry_field1 = tk.Entry(width=30)
        entry_field1.grid(row=1, sticky="e", padx=70)

        # ENTRY FIELD 3
        prompt3 = tk.Label(text="Username (email/phone/etc)", font=("Arial", "12"), fg=LABEL_COLOR)
        prompt3.grid(row=2, sticky="w", padx=10)
        prompt3.configure(background=GUI_BG_COLOR)
        entry_field3 = tk.Entry(width=30)
        entry_field3.grid(row=2, sticky="e", padx=70)

        # ENTRY FIELD 2
        prompt2 = tk.Label(text="Password", font=("Arial", "12"), fg=LABEL_COLOR)
        prompt2.grid(row=3, sticky="w", padx=10, pady=20)
        prompt2.configure(background=GUI_BG_COLOR)
        entry_field2 = tk.Entry(width=30)
        entry_field2.grid(row=3, sticky="e", padx=70)

        # ENTRY FIELD 4
        prompt5 = tk.Label(text="URL(optional)", font=("Arial", "12"), fg=LABEL_COLOR)
        prompt5.grid(row=4, sticky="w", padx=10)
        prompt5.configure(background=GUI_BG_COLOR)
        entry_field4 = tk.Entry(width=30)
        entry_field4.grid(row=4, sticky="e", padx=70)

        _prompt = tk.Label(text="Saving password Mode", font=("Arial", "12"), fg=LABEL_COLOR)
        _prompt.grid(row=5, sticky="w", padx=10)
        _prompt.configure(background=GUI_BG_COLOR)

        # option menu 1
        var = tk.StringVar(window)
        var.set("Mode")
        option = tk.OptionMenu(window, var, "Plain/Text", "Encrypify")
        option.configure(font=("Arial", "10", "bold"), width=10, bg="black", fg="white")
        option.grid(row=5, stick="e", pady=20, padx=140)

        # button 1
        button1 = tk.Button(text="Save Password",
                            command=partial(save_data, entry_field1, entry_field3, entry_field2,
                                            entry_field4, var, window),
                            font=("Times", "12", "bold"), bg=TITLE_COLOR, fg="black")
        button1.grid(row=6, sticky="e", padx=140)

        show_down_menu(window)
        button1 = tk.Button(text="Disclaimer", font=("Arial", "10"), command=show_disclaimer)
        button1.configure(bg="black", fg="#ffff66")
        button1.grid(row=11, pady=100, sticky="w", padx=200)

        window.mainloop()


Password()
