import time

class PomodoroTimer:
    def __init__(self, work_time=25, break_time=5):
        """Initialize the Pomodoro Timer with default durations (25 min work, 5 min break)."""
        self.work_time = work_time * 60  # in seconds
        self.break_time = break_time * 60  # in seconds

    def start_work_session(self):
        """
        Start a Pomodoro work session.
        :return: None
        """
        print(f"Starting work session for {self.work_time // 60} minutes.")
        time.sleep(self.work_time)
        print("Work session ended. Time for a break!")

    def start_break(self):
        """
        Start a break session.
        :return: None
        """
        print(f"Starting break for {self.break_time // 60} minutes.")
        time.sleep(self.break_time)
        print("Break ended. Back to work!")
