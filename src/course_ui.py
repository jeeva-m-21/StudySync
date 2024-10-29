import tkinter as tk
from tkinter import messagebox
from database import Database  # Assuming you have a Database class for DB operations

class CourseManagementUI:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Course Management")
        self.username = username

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
        # Open a new window to manage the selected course
        course_window = tk.Toplevel(self.master)
        course_window.title(f"Managing {course}")

        # Here, you can implement further management options for the selected course
        tk.Label(course_window, text=f"You are managing the course: {course}").pack(pady=10)

        # Close button
        tk.Button(course_window, text="Close", command=course_window.destroy).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManagementUI(root, "test_user")  # Replace with an actual username
    root.mainloop()
