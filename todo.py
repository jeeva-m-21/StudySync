import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END
import mysql.connector

class TodoManager:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("To-Do Manager")
        self.root.configure(bg='lightblue')  # Set the background color

        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task, bg='blue', fg='white')
        self.add_task_button.pack(pady=5)

        self.tasks_listbox = Listbox(self.root, width=50, bg='white', selectbackground='lightgrey')
        self.tasks_listbox.pack(pady=10)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tasks_listbox.yview)

        self.tasks_listbox.bind("<Double-Button-1>", self.toggle_task)

        self.db_connection = self.connect_to_database()
        self.load_tasks()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Smks1_1030",
                database="study_sync_db"
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def add_task(self):
        task = self.task_entry.get()
        if task:
            cursor = self.db_connection.cursor()
            query = "INSERT INTO tasks (username, task) VALUES (%s, %s)"
            values = (self.username, task)
            try:
                cursor.execute(query, values)
                self.db_connection.commit()
                cursor.close()
                self.load_tasks()
                self.task_entry.delete(0, END)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def load_tasks(self):
        self.tasks_listbox.delete(0, END)  # Clear the listbox
        cursor = self.db_connection.cursor()
        query = "SELECT task, completed FROM tasks WHERE username = %s"
        cursor.execute(query, (self.username,))
        tasks = cursor.fetchall()

        for task, completed in tasks:
            display_task = f"[{'x' if completed else ' '}] {task}"
            self.tasks_listbox.insert(END, display_task)

        cursor.close()

    def toggle_task(self, event):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            selected_task = self.tasks_listbox.get(selected_index).strip()
            task_name = selected_task[4:]  # Remove checkbox part
            is_completed = selected_task[1] == 'x'

            cursor = self.db_connection.cursor()
            query = "UPDATE tasks SET completed = %s WHERE username = %s AND task = %s"
            cursor.execute(query, (not is_completed, self.username, task_name))
            self.db_connection.commit()
            cursor.close()
            self.load_tasks()

    def run(self):
        self.root.mainloop()

def todorunner(username):
    app = TodoManager(username)
    app.run()



