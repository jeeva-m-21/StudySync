
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import mysql.connector
import os
import tempfile
import webbrowser

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="1059",  # Replace with your MySQL password
        database="study_sync_db"  # Replace with your database name
    )

# Function to verify if the username exists in the users table
def user_exists(username):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        return cursor.fetchone()[0] > 0  # Returns True if the user exists
    except Exception as e:
        print(f"Error checking user: {e}")
        return False
    finally:
        cursor.close()
        db.close()

# Function to add PDF to database for a specific user
def add_pdf_to_db(username, title, pdf_data):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        query = "INSERT INTO materials (username, title, file_data) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, title, pdf_data))
        db.commit()
        print(f"Successfully added '{title}' for user '{username}'.")  # Debugging info
        return True
    except Exception as e:
        print(f"Error adding PDF: {e}")  # Print error message for debugging
        return False
    finally:
        cursor.close()
        db.close()

# Function to fetch PDF titles from database for a specific user
def get_pdf_titles(username):
    titles = []
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT title FROM materials WHERE username = %s", (username,))
        titles = [row[0] for row in cursor.fetchall()]  # Fetch all rows
        print(f"Fetched titles: {titles}")  # Debugging info
    except Exception as e:
        print(f"Error fetching titles: {e}")
    finally:
        cursor.close()
        db.close()
    return titles

# Function to retrieve and open PDF from database for a specific user
def open_pdf_from_db(username, title):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT file_data FROM materials WHERE username = %s AND title = %s", (username, title))
        result = cursor.fetchone()  # Fetch the single result
        if result:
            pdf_data = result[0]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_data)
                temp_path = temp_file.name
            webbrowser.open(temp_path)
            print(f"Opened PDF: {temp_path}")  # Debugging info
        else:
            print(f"No PDF found for '{title}'")  # Debugging info
    except Exception as e:
        print(f"Error opening PDF: {e}")
    finally:
        cursor.close()
        db.close()

# Main application class
class PDFStorageApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        # Verify that the username exists
        if not user_exists(self.username):
            messagebox.showerror("User Error", f"The user '{self.username}' does not exist.")
            self.root.destroy()  # Exit the application if user doesn't exist
            return

        self.root.title(f"PDF Storage App for {self.username}")
        self.root.geometry("600x400")

        # Title Label
        tk.Label(root, text="Drag & Drop PDFs or Browse to Add", font=("Arial", 14)).pack(pady=10)

        # PDF Listbox
        self.pdf_listbox = tk.Listbox(root, width=50, height=10)
        self.pdf_listbox.pack(pady=10)

        # Browse Button
        tk.Button(root, text="Browse Files", command=self.browse_file).pack(pady=5)

        # View Button
        tk.Button(root, text="View Files", command=self.load_pdf_titles).pack(pady=5)
        self.pdf_listbox.bind("<Double-1>", self.view_pdf)  # Double-click to view

        # Drag-and-drop registration
        root.drop_target_register(DND_FILES)
        root.dnd_bind("<<Drop>>", self.drop_file)

    # Browse files
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.save_pdf(file_path)

    # Handle file drop
    def drop_file(self, event):
        file_path = event.data.strip("{}")  # Remove curly braces added by TkinterDnD
        if os.path.isfile(file_path) and file_path.lower().endswith(".pdf"):
            self.save_pdf(file_path)
        else:
            messagebox.showwarning("File Error", "Please drop a valid PDF file.")

    # Save PDF to database for the specific user
    def save_pdf(self, file_path):
        title = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            pdf_data = file.read()

        if add_pdf_to_db(self.username, title, pdf_data):
            messagebox.showinfo("Success", f"'{title}' has been added to the database.")
            self.pdf_listbox.insert(tk.END, title)
        else:
            messagebox.showerror("Error", f"Could not save '{title}' to the database.")

    # Load PDF titles into listbox for the specific user
    def load_pdf_titles(self):
        self.pdf_listbox.delete(0, tk.END)  # Clear listbox
        titles = get_pdf_titles(self.username)
        self.pdf_listbox.delete(0, tk.END)  # Clear previous titles
        for title in titles:
            self.pdf_listbox.insert(tk.END, title)

    # View selected PDF for the specific user
    def view_pdf(self, event):
        selection = self.pdf_listbox.curselection()
        if selection:
            title = self.pdf_listbox.get(selection[0])
            open_pdf_from_db(self.username, title)

def run_materials(username):
    root = TkinterDnD.Tk()
    app = PDFStorageApp(root, username)
    root.mainloop()
