import tkinter as tk
from tkinter import messagebox
import time
import pickle

# File to store user database
DATABASE_FILE = "user_database.pkl"
PERSONAL_INFO_FILE = "personal_info.pkl"

# Lockout duration in seconds
LOCKOUT_DURATION = 60

def load_user_database():
    try:
        with open(DATABASE_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def save_user_database(user_database):
    with open(DATABASE_FILE, "wb") as file:
        pickle.dump(user_database, file)

def load_personal_info():
    try:
        with open(PERSONAL_INFO_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def save_personal_info(personal_info):
    with open(PERSONAL_INFO_FILE, "wb") as file:
        pickle.dump(personal_info, file)

def register_new_user():
    def register():
        username = username_entry.get()
        password = password_entry.get()

        if username in user_database:
            messagebox.showerror("Error", "Username already taken. Please choose a unique username.")
        else:
            user_database[username] = {"password": password, "attempts_left": 3, "last_attempt_time": 0}
            save_user_database(user_database)
            messagebox.showinfo("Success", "User registered successfully!")
            show_homepage()

    homepage_frame.pack_forget()
    register_frame.pack()

    register_label = tk.Label(register_frame, text="New User Registration", font=("Helvetica", 16))
    register_label.grid(row=0, column=0, columnspan=2, pady=10)

    username_label = tk.Label(register_frame, text="Username:")
    username_label.grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(register_frame)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = tk.Label(register_frame, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(register_frame, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)

def user_login():
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username not in user_database:
            messagebox.showerror("Error", "Username not found. Please register or enter a valid username.")
            return

        user_data = user_database[username]
        if user_data["attempts_left"] == 0 and time.time() - user_data["last_attempt_time"] < LOCKOUT_DURATION:
            messagebox.showerror("Error", "You are locked out. Please try again later.")
            return

        if user_data["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            user_data["attempts_left"] = 3  # Reset attempts left on successful login
            save_user_database(user_database)
            show_personal_info(root, username)  # Pass root as an argument
        else:
            user_data["attempts_left"] -= 1
            if user_data["attempts_left"] > 0:
                messagebox.showerror("Error", f"Sorry, incorrect password. Attempts Left: {user_data['attempts_left']}")
            else:
                user_data["last_attempt_time"] = time.time()
                messagebox.showerror("Error", "You have exhausted all attempts. You will be locked out for one minute.")
                save_user_database(user_database)
                show_homepage()

    homepage_frame.pack_forget()
    login_frame.pack()

    login_label = tk.Label(login_frame, text="User Login", font=("Helvetica", 16))
    login_label.grid(row=0, column=0, columnspan=2, pady=10)

    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)

def show_homepage():
    login_frame.pack_forget()
    register_frame.pack_forget()
    homepage_frame.pack()

def show_personal_info(root, username):  # Pass root as an argument
    personal_info = load_personal_info()
    if username not in personal_info:
        personal_info[username] = {"full_name": "", "email": "", "profession": ""}
        save_personal_info(personal_info)

    personal_info_frame = tk.Frame(root)
    personal_info_frame.pack()

    personal_info_label = tk.Label(personal_info_frame, text=f"Welcome to your Profile, {username}", font=("Helvetica", 16))
    personal_info_label.grid(row=0, column=0, columnspan=2, pady=10)

    user_details_label = tk.Label(personal_info_frame, text="Personal Details", font=("Helvetica", 14))
    user_details_label.grid(row=1, column=0, columnspan=2, pady=5)

    full_name_label = tk.Label(personal_info_frame, text="Full Name:")
    full_name_label.grid(row=2, column=0, padx=10, pady=5)
    full_name_entry = tk.Entry(personal_info_frame)
    full_name_entry.grid(row=2, column=1, padx=10, pady=5)
    full_name_entry.insert(0, personal_info[username]["full_name"])

    email_label = tk.Label(personal_info_frame, text="Email:")
    email_label.grid(row=3, column=0, padx=10, pady=5)
    email_entry = tk.Entry(personal_info_frame)
    email_entry.grid(row=3, column=1, padx=10, pady=5)
    email_entry.insert(0, personal_info[username]["email"])

    profession_label = tk.Label(personal_info_frame, text="Profession:")
    profession_label.grid(row=4, column=0, padx=10, pady=5)
    profession_entry = tk.Entry(personal_info_frame)
    profession_entry.grid(row=4, column=1, padx=10, pady=5)
    profession_entry.insert(0, personal_info[username]["profession"])

    def save_changes():
        personal_info[username]["full_name"] = full_name_entry.get()
        personal_info[username]["email"] = email_entry.get()
        personal_info[username]["profession"] = profession_entry.get()
        save_personal_info(personal_info)
        messagebox.showinfo("Success", "Changes saved successfully!")
        personal_info_frame.destroy()
        show_homepage()

    save_button = tk.Button(personal_info_frame, text="Save Changes", command=save_changes)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

def main():
    global user_database
    user_database = load_user_database()

    global root
    root = tk.Tk()
    root.title("Simple Authentication System")
    root.geometry("675x450")  # Set window size to 90% height and 75% width

    global homepage_frame
    homepage_frame = tk.Frame(root)

    homepage_label = tk.Label(homepage_frame, text="Welcome to Simple Authentication System", pady=10)
    homepage_label.pack()

    register_button = tk.Button(homepage_frame, text="New User Registration", command=register_new_user)
    register_button.pack()

    login_button = tk.Button(homepage_frame, text="User Login", command=user_login)
    login_button.pack()

    global register_frame
    register_frame = tk.Frame(root)

    global login_frame
    login_frame = tk.Frame(root)

    show_homepage()

    root.mainloop()

if __name__ == "__main__":
    main()
