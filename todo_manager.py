from database import Database

class ToDoManager:
    def __init__(self, db: Database):
        """Initialize ToDoManager with a database connection."""
        self.db = db

    def add_task(self, course_id: int, task_description: str):
        """
        Add a task to a specific course's to-do list.
        :param course_id: ID of the course.
        :param task_description: Description of the task.
        """
        self.db.add_task(course_id, task_description)

    def get_tasks(self, course_id: int) -> list:
        """
        Get all tasks related to a course.
        :param course_id: ID of the course.
        :return: A list of tasks.
        """
        return self.db.get_tasks_by_course(course_id)

    def mark_task_complete(self, task_id: int):
        """
        Mark a task as complete.
        :param task_id: ID of the task to be marked as complete.
        """
        self.db.update_task_status(task_id, completed=True)
