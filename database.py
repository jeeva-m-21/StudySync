import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        """
        Initialize the database connection and cursor.
        """
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',  # Change this to your MySQL user
                password='1059',  # Change this to your MySQL password
                database='studysync'  # Make sure this database exists
            )
            if self.conn.is_connected():
                print("Successfully connected to the database")
                self.cursor = self.conn.cursor()
                self.create_tables()  # Create tables on initialization
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def create_tables(self):
        """
        Create necessary tables in the database.
        """
        try:
            # Create users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            ''')

            # Create courses table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    course_name VARCHAR(255) NOT NULL,
                    course_desc TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

            # Create tasks table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_id INT NOT NULL,
                    task_desc TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''')

            # Create recaps table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS recaps (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_id INT NOT NULL,
                    recap_text TEXT NOT NULL,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''')

            # Create materials table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS materials (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_id INT NOT NULL,
                    file_path VARCHAR(255) NOT NULL,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''')

            # Commit changes
            self.conn.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")

    # User-related functions
    def add_user(self, username: str, password: str):
        """
        Add a new user to the database.
        """
        try:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.cursor.execute(query, (username, password))
            self.conn.commit()
        except Error as e:
            print(f"Error adding user: {e}")

    def get_user(self, username: str, password: str):
        """
        Retrieve user information based on username and password.
        """
        try:
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None

    # Course-related functions
    def add_course(self, user_id: int, course_name: str, course_desc: str):
        if not self.conn.is_connected():
            print("Lost connection to the database. Reconnecting...")
            self.__init__()  # reconnect

        try:
            query = "INSERT INTO courses (user_id, course_name, course_desc) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (user_id, course_name, course_desc))
            self.conn.commit()
            print("Course added successfully.")
        except Error as e:
            print(f"Error adding course: {e}")
            self.conn.rollback()  # Rollback in case of error

    def get_courses(self, user_id: int):
        """
        Get all courses for a specific user.
        """
        try:
            query = "SELECT * FROM courses WHERE user_id=%s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving courses: {e}")
            return []

    # Task-related functions
    def add_task(self, course_id: int, task_desc: str):
        """
        Add a new task to the to-do list.
        """
        try:
            query = "INSERT INTO tasks (course_id, task_desc, is_completed) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (course_id, task_desc, False))
            self.conn.commit()
        except Error as e:
            print(f"Error adding task: {e}")

    def get_tasks(self, course_id: int):
        """
        Get all tasks for a specific course.
        """
        try:
            query = "SELECT * FROM tasks WHERE course_id=%s"
            self.cursor.execute(query, (course_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving tasks: {e}")
            return []

    # Recap-related functions
    def add_recap(self, course_id: int, recap_text: str):
        """
        Add a recap entry for a course.
        """
        try:
            query = "INSERT INTO recaps (course_id, recap_text) VALUES (%s, %s)"
            self.cursor.execute(query, (course_id, recap_text))
            self.conn.commit()
        except Error as e:
            print(f"Error adding recap: {e}")

    def get_recaps_by_course(self, course_id: int):
        """
        Retrieve all recaps for a specific course.
        """
        try:
            query = "SELECT * FROM recaps WHERE course_id=%s"
            self.cursor.execute(query, (course_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving recaps: {e}")
            return []

    # Study material-related functions
    def store_study_material(self, course_id: int, file_path: str):
        """
        Store study material file paths for a course.
        """
        try:
            query = "INSERT INTO materials (course_id, file_path) VALUES (%s, %s)"
            self.cursor.execute(query, (course_id, file_path))
            self.conn.commit()
        except Error as e:
            print(f"Error storing study material: {e}")

    def get_materials_by_course(self, course_id: int):
        """
        Retrieve all study materials for a specific course.
        """
        try:
            query = "SELECT * FROM materials WHERE course_id=%s"
            self.cursor.execute(query, (course_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving materials: {e}")
            return []

    def close_connection(self):
        """
        Close the connection to the MySQL database.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
