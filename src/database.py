import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        """Create a database connection."""
        try:
            connection = mysql.connector.connect(
                host='localhost',  # e.g., 'localhost'
                user='root',  # e.g., 'root'
                password='1059',
                database='study_sync_db'  # e.g., 'study_sync_db'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()

    @staticmethod
    def create_user(username, password, email):
        """Register a new user in the database."""
        try:
            db = Database()
            cursor = db.connection.cursor()
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            db.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            db.close_connection()

    @staticmethod
    def get_user(username, password):
        """Retrieve user data for login validation."""
        try:
            db = Database()
            cursor = db.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()  # Returns a dictionary if found, else None
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            db.close_connection()

    @staticmethod
    def get_courses_by_user(username):
        """Get a list of courses for a specific user."""
        try:
            db = Database()
            cursor = db.connection.cursor()
            query = "SELECT course_name FROM courses WHERE username = %s"
            cursor.execute(query, (username,))
            return [row[0] for row in cursor.fetchall()]  # Return a list of course names
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            db.close_connection()

    @staticmethod
    def add_course(username, course_name):
        """Add a new course for the user."""
        try:
            db = Database()
            cursor = db.connection.cursor()
            query = "INSERT INTO courses (username, course_name) VALUES (%s, %s)"
            cursor.execute(query, (username, course_name))
            db.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            db.close_connection()

    @staticmethod
    def delete_course(username, course_name):
        """Delete a specified course for the user."""
        try:
            db = Database()
            cursor = db.connection.cursor()
            query = "DELETE FROM courses WHERE username = %s AND course_name = %s"
            cursor.execute(query, (username, course_name))
            db.connection.commit()
            return cursor.rowcount > 0  # Returns True if a row was deleted
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            db.close_connection()
