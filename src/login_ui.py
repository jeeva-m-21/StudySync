import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database  # Assuming you have a Database class for DB operations
from course_ui import CourseManagementUI  # Import course management UI

class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        # Username and password labels and entries
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Login and Register buttons
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if Database.get_user(username, password):  # Replace with your DB login method
            messagebox.showinfo("Login Successful", "Welcome back!")
            self.master.destroy()  # Close login window
            self.open_course_management(username)  # Pass username to the course management page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = simpledialog.askstring("Register", "Enter a new username:")
        if username:
            password = simpledialog.askstring("Register", "Enter a password:", show='*')
            if password:
                email = simpledialog.askstring("Register", "Enter your email:")
                if email:
                    if Database.create_user(username, password, email):  # Replace with your DB registration method
                        messagebox.showinfo("Registration Successful", "You can now log in.")
                    else:
                        messagebox.showerror("Registration Failed", "Username already exists.")

    def open_course_management(self, username):
        root = tk.Tk()
        CourseManagementUI(root, username)  # Initialize the course management page with the username
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()
