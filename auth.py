from database import Database

class Auth:
    def __init__(self, db: Database):
        """Initialize Auth class with a database connection."""
        self.db = db

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate the user by verifying credentials.
        :param username: Username input.
        :param password: Password input.
        :return: True if credentials match, False otherwise.
        """
        user = self.db.get_user(username, password)
        return user is not None

    def signup(self, username: str, password: str) -> bool:
        """
        Register a new user in the database.
        :param username: New username.
        :param password: New password.
        :return: True on successful signup.
        """
        if not self.db.user_exists(username):
            self.db.add_user(username, password)
            return True
        return False
