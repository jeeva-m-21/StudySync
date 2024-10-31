import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkFont
from database import Database  # Assuming you have a Database class for DB operations
from course_ui import CourseManagementUI  # Import course management UI

class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x300")  # Set the window size
        self.master.config(bg="#282c34")  # Set background color to dark

        # Custom font
        self.font = tkFont.Font(family="Helvetica", size=12)

        # Frame for the login form with rounded corners
        self.frame = tk.Frame(master, bg="#3c4043", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

        # Username and password labels and entries with improved styling
        self.username_label = tk.Label(self.frame, text="Username:", font=self.font, bg="#3c4043", fg="white")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=self.font, width=30, bg="#ffffff", fg="black", borderwidth=2, relief="groove")
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.frame, text="Password:", font=self.font, bg="#3c4043", fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.frame, font=self.font, show="*", width=30, bg="#ffffff", fg="black", borderwidth=2, relief="groove")
        self.password_entry.pack(pady=5)

        # Login and Register buttons with rounded corners and hover effects
        self.login_button = tk.Button(self.frame, text="Login", command=self.login, bg="#4CAF50", fg="white", font=self.font, relief="flat")
        self.login_button.pack(pady=10, fill=tk.X)

        self.register_button = tk.Button(self.frame, text="Register", command=self.register, bg="#2196F3", fg="white", font=self.font, relief="flat")
        self.register_button.pack(pady=10, fill=tk.X)

        # Add hover effect to buttons
        self.login_button.bind("<Enter>", lambda e: self.on_enter(self.login_button, "#45a049"))
        self.login_button.bind("<Leave>", lambda e: self.on_leave(self.login_button, "#4CAF50"))
        self.register_button.bind("<Enter>", lambda e: self.on_enter(self.register_button, "#1E88E5"))
        self.register_button.bind("<Leave>", lambda e: self.on_leave(self.register_button, "#2196F3"))

    def on_enter(self, button, color):
        button.config(bg=color)

    def on_leave(self, button, color):
        button.config(bg=color)

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

root = tk.Tk()
app = LoginUI(root)
root.mainloop()

