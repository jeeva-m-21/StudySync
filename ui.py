import tkinter as tk
from tkinter import messagebox, filedialog
from auth import Auth
from course_manager import CourseManager
from todo_manager import ToDoManager
from pomodoro_timer import PomodoroTimer
from recap_material import RecapMaterial
from database import Database

class StudySyncApp:
    def __init__(self):
        # Initialize the Tkinter root window
        self.root = tk.Tk()
        self.root.title("StudySync")

        # Initialize database connection and other modules
        self.db = Database()
        self.auth = Auth(self.db)
        self.course_manager = CourseManager(self.db)
        self.todo_manager = ToDoManager(self.db)
        
        self.recap_material = RecapMaterial(self.db)

        self.user_id = None  # Logged-in user's ID

        self.show_login_screen()  # Start with login screen
        self.root.mainloop()

    def show_login_screen(self):
        """Display the login/signup window."""
        self.clear_window()
        tk.Label(self.root, text="Welcome to StudySync").pack()

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def handle_login():
            username = username_entry.get()
            password = password_entry.get()
            if self.auth.login(username, password):
                self.user_id = self.db.get_user(username, password)[0]
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

        def handle_signup():
            username = username_entry.get()
            password = password_entry.get()
            if self.auth.signup(username, password):
                messagebox.showinfo("Signup Successful", "You can now log in.")
            else:
                messagebox.showerror("Signup Failed", "Username already exists.")

        tk.Button(self.root, text="Login", command=handle_login).pack()
        tk.Button(self.root, text="Sign Up", command=handle_signup).pack()

    def show_dashboard(self):
        """Display the main dashboard where users can manage courses, tasks, and more."""
        self.clear_window()

        tk.Label(self.root, text="Dashboard").pack()

        tk.Button(self.root, text="Manage Courses", command=self.show_courses).pack()
        tk.Button(self.root, text="Manage To-Do List", command=self.show_todo).pack()
        tk.Button(self.root, text="Start Pomodoro Timer", command=self.show_pomodoro_timer).pack()
        tk.Button(self.root, text="Add Recap", command=self.show_recap).pack()

    def show_courses(self):
        """Display the course management window."""
        self.clear_window()
        tk.Label(self.root, text="Courses").pack()

        # Add course form
        tk.Label(self.root, text="Course Name").pack()
        course_name_entry = tk.Entry(self.root)
        course_name_entry.pack()

        tk.Label(self.root, text="Description").pack()
        course_desc_entry = tk.Entry(self.root)
        course_desc_entry.pack()

        def add_course():
            course_name = course_name_entry.get()
            course_desc = course_desc_entry.get()
            if course_name and course_desc:
                self.course_manager.add_course(self.user_id, course_name, course_desc)
                messagebox.showinfo("Success", "Course added successfully!")
                self.show_courses()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(self.root, text="Add Course", command=add_course).pack()

        # List all courses
        courses = self.course_manager.get_courses(self.user_id)
        for course in courses:
            tk.Label(self.root, text=f"{course[1]} - {course[2]}").pack()

        tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard).pack()

    def show_todo(self):
        """Display the to-do list management window."""
        self.clear_window()
        tk.Label(self.root, text="To-Do List").pack()

        # Task entry form
        tk.Label(self.root, text="Course ID").pack()
        course_id_entry = tk.Entry(self.root)
        course_id_entry.pack()

        tk.Label(self.root, text="Task Description").pack()
        task_desc_entry = tk.Entry(self.root)
        task_desc_entry.pack()

        def add_task():
            course_id = course_id_entry.get()
            task_desc = task_desc_entry.get()
            if course_id and task_desc:
                self.todo_manager.add_task(int(course_id), task_desc)
                messagebox.showinfo("Success", "Task added successfully!")
                self.show_todo()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(self.root, text="Add Task", command=add_task).pack()

        # List all tasks
        tasks = self.todo_manager.get_tasks(int(course_id_entry.get() or 0))
        for task in tasks:
            tk.Label(self.root, text=f"{task[1]} - {'Completed' if task[2] else 'Pending'}").pack()

        tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard).pack()

    def show_pomodoro_timer(self):
       self.pomodoro_timer = PomodoroTimer()
    def show_recap(self):
        """Display recap input window."""
        self.clear_window()
        tk.Label(self.root, text="Add Recap").pack()

        tk.Label(self.root, text="Course ID").pack()
        course_id_entry = tk.Entry(self.root)
        course_id_entry.pack()

        tk.Label(self.root, text="Recap Text").pack()
        recap_entry = tk.Entry(self.root)
        recap_entry.pack()

        def add_recap():
            course_id = course_id_entry.get()
            recap_text = recap_entry.get()
            if course_id and recap_text:
                self.recap_material.add_recap(int(course_id), recap_text)
                messagebox.showinfo("Success", "Recap added successfully!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(self.root, text="Add Recap", command=add_recap).pack()

        tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard).pack()

    def clear_window(self):
        """Clear the current window's content to load a new view."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    StudySyncApp()