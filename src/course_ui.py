import tkinter as tk
from tkinter import messagebox
from tkinter import font
from database import Database  # Assuming you have a Database class for DB operations
from pomodoro import Pomodoro
import notes
import materials
import recordings
import todo
class CourseManagementUI:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Course Management")
        self.username = username
        global username1
        username1=username
        # Title
        title_label = tk.Label(master, text="Manage Your Courses")
        title_label.pack(pady=10)

        # Frame to display courses
        self.course_frame = tk.Frame(master)
        self.course_frame.pack(pady=5)

        # Load and display courses
        self.display_courses()

        # Buttons for adding and managing courses
        self.add_course_button = tk.Button(master, text="Add Course", command=self.add_course)
        self.add_course_button.pack(pady=5)

        self.delete_course_button = tk.Button(master, text="Delete Course", command=self.delete_course)
        self.delete_course_button.pack(pady=5)

       # self.manage_course_button = tk.Button(master, text="Manage Course", command=self.manage_course)
        #self.manage_course_button.pack(pady=5)

    def display_courses(self):
        # Clear previous course display
        for widget in self.course_frame.winfo_children():
            widget.destroy()

        # Fetch courses from the database for the current user
        courses = Database.get_courses_by_user(self.username)
        for course in courses:
            course_button = tk.Button(self.course_frame, text=course, command=lambda c=course: self.manage_course(c))
            course_button.pack(pady=2)

    def add_course(self):
        course_name = tk.simpledialog.askstring("Add Course", "Enter course name:")
        if course_name:
            if Database.add_course(self.username, course_name):  # Method to add a course to the DB
                messagebox.showinfo("Success", "Course added successfully!")
                self.display_courses()  # Refresh course list
            else:
                messagebox.showerror("Error", "Failed to add course.")

    def delete_course(self):
        course_name = tk.simpledialog.askstring("Delete Course", "Enter course name to delete:")
        if course_name:
            if Database.delete_course(self.username, course_name):  # Method to delete a course from the DB
                messagebox.showinfo("Success", "Course deleted successfully!")
                self.display_courses()  # Refresh course list
            else:
                messagebox.showerror("Error", "Failed to delete course.")

 

    def manage_course(self, course):
    
        course_window = tk.Toplevel(self.master)
        course_window.title(f"Managing {course}")
        course_window.geometry("400x300")
        course_window.configure(bg="#f0f4f7")

    # Header Label
        header_font = font.Font(family="Helvetica", size=14, weight="bold")
        tk.Label(
        course_window, 
        text=f"You are managing the course: {course}",
        bg="#f0f4f7", 
        fg="#333333", 
        font=header_font
        ).pack(pady=15)

    # Define placeholder functions
        def start_pomodoro():
            pomodoro_window = tk.Toplevel(self.master)  # Create a new top-level window
            pomodoro_window.title("Pomodoro Timer")  # Set title for the top-level window
            pomo_app = Pomodoro(pomodoro_window)  # Initialize Pomodoro with the top-level window
            pomo_app.main()  # Start the Pomodoro main method


    
        def manage_notes():
            notes.start_notes_app(username1)

        def add_materials():
            materials.run_materials(username1)
 
        def add_recording():
           recordings.recordrunner(username1)  # Placeholder for actual functionality
    
        def manage_todo():
            todo.todorunner(username1)

    # Button Style
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        button_bg = "#4a90e2"
        button_fg = "#ffffff"
        button_hover_bg = "#3a7ad9"
    
    # Create each button with enhanced styling
        buttons = [
            ("Start Pomodoro", start_pomodoro),
            ("Manage Notes", manage_notes),
            ("Add Materials", add_materials),
            ("Add Recording", add_recording),
            ("Manage To-Do", manage_todo)
        ]
    
        for text, command in buttons:
            button = tk.Button(
            course_window,
            text=text,
            command=command,
            bg=button_bg,
            fg=button_fg,
            font=button_font,
            activebackground=button_hover_bg,
            activeforeground=button_fg,
            relief="flat",
            padx=10,
            pady=5,
            width=20
            )
            button.pack(pady=5)
    
    # Close Button
        tk.Button(
        course_window, 
        text="Close", 
        command=course_window.destroy,
        bg="#e74c3c", 
        fg="#ffffff", 
        font=button_font,
        activebackground="#c0392b",
        relief="flat",
        padx=10,
        pady=5,
        width=20
        ).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManagementUI(root, "test_user")  # Replace with an actual username
    root.mainloop()
