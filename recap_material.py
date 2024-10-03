from database import Database

class RecapMaterial:
    def __init__(self, db: Database):
        """Initialize RecapMaterial with a database connection."""
        self.db = db

    def add_recap(self, course_id: int, recap_text: str):
        """
        Add a daily recap for a specific course.
        :param course_id: ID of the course.
        :param recap_text: Text of the recap.
        """
        self.db.add_recap(course_id, recap_text)

    def store_material(self, course_id: int, file_path: str):
        """
        Store study material (e.g., PDF, images).
        :param course_id: ID of the course.
        :param file_path: Path to the material file.
        """
        self.db.store_study_material(course_id, file_path)

    def get_materials(self, course_id: int) -> list:
        """
        Retrieve all stored materials for a course.
        :param course_id: ID of the course.
        :return: List of file paths.
        """
        return self.db.get_materials_by_course(course_id)
