from database import Database

class CourseManager:
    def __init__(self, db: Database):
        """Initialize CourseManager with a database connection."""
        self.db = db

    def add_course(self, user_id: int, course_name: str, description: str):
        """
        Add a new course to the system.
        :param user_id: ID of the user who is adding the course.
        :param course_name: Name of the course.
        :param description: Course description or notes.
        """
        self.db.add_course(user_id, course_name, description)

    def get_courses(self, user_id: int) -> list:
        """
        Retrieve all courses for a user.
        :param user_id: ID of the user.
        :return: A list of courses.
        """
        return self.db.get_courses_by_user(user_id)

    def update_course_progress(self, course_id: int, progress: str):
        """
        Update the daily progress of a course.
        :param course_id: ID of the course.
        :param progress: Progress description.
        """
        self.db.update_course_progress(course_id, progress)
