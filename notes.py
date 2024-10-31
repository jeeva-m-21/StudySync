import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import mysql.connector

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='Smks1_1030',  # Replace with your MySQL password
        database='study_sync_db'
    )

def user_exists(username):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user[0] if user else None

def add_note(user_id, title, content):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    db.commit()
    cursor.close()
    db.close()

def get_notes(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()
    cursor.close()
    db.close()
    return notes

def update_note(note_id, title, content):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
    db.commit()
    cursor.close()
    db.close()

# GUI Class
class NotesApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.user_id = self.get_user_id(username)

        if self.user_id is None:
            messagebox.showerror("User Error", "User does not exist.")
            master.destroy()
            return

        self.master.title("Notes App")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        # Frame for Listbox and Buttons
        frame = tk.Frame(master, bg="#f0f0f0")
        frame.pack(pady=20)

        self.notes_listbox = tk.Listbox(frame, width=50, height=15, font=("Arial", 12), bg="#ffffff", selectmode=tk.SINGLE)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.notes_listbox.yview)

        # Buttons Frame
        buttons_frame = tk.Frame(master, bg="#f0f0f0")
        buttons_frame.pack(pady=10)

        self.add_button = ttk.Button(buttons_frame, text="Add Note", command=self.add_note)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(buttons_frame, text="Edit Note", command=self.edit_note)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.load_notes()

    def get_user_id(self, username):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        return user[0] if user else None

    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)
        notes = get_notes(self.user_id)
        for note in notes:
            self.notes_listbox.insert(tk.END, f"{note[2]}: {note[3]}")  # Displaying title and content

    def add_note(self):
        title = simpledialog.askstring("Title", "Enter note title:")
        content = simpledialog.askstring("Content", "Enter note content:")
        if title and content:
            add_note(self.user_id, title, content)
            self.load_notes()
        else:
            messagebox.showwarning("Input Error", "Both title and content are required.")

    def edit_note(self):
        selected_note = self.notes_listbox.curselection()
        if not selected_note:
            messagebox.showwarning("Selection Error", "Please select a note to edit.")
            return

        note_id = selected_note[0] + 1  # Adjust based on your database indexing
        title = simpledialog.askstring("Edit Title", "Enter new note title:")
        content = simpledialog.askstring("Edit Content", "Enter new note content:")
        if title and content:
            update_note(note_id, title, content)
            self.load_notes()
        else:
            messagebox.showwarning("Input Error", "Both title and content are required.")

def start_notes_app(username):
    root = tk.Tk()
    app = NotesApp(root, username)
    root.mainloop()




