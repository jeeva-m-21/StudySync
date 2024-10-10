import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, work_time=25, break_time=5):
        """Initialize the Pomodoro Timer with default durations (25 min work, 5 min break)."""
        self.work_time = work_time * 60  # in seconds
        self.break_time = break_time * 60  # in seconds
        self.timer_running = False

        # Create GUI elements
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.config(bg="#f7f5dd")

        # Title Label
        self.label = tk.Label(self.root, text="Pomodoro Timer", font=("Helvetica", 26, "bold"), bg="#f7f5dd", fg="#444444")
        self.label.pack(pady=20)

        # Time Display
        self.time_label = tk.Label(self.root, text=self.format_time(self.work_time), font=("Helvetica", 50), bg="#f7f5dd", fg="#e7305b")
        self.time_label.pack(pady=20)

        # Button Frame for better layout
        button_frame = tk.Frame(self.root, bg="#f7f5dd")
        button_frame.pack(pady=10)

        # Start Work Button
        self.start_work_button = tk.Button(button_frame, text="Start Work Session", command=self.start_work_session,
                                           font=("Helvetica", 14), bg="#9bdeac", fg="white", width=15)
        self.start_work_button.grid(row=0, column=0, padx=5)

        # Start Break Button
        self.start_break_button = tk.Button(button_frame, text="Start Break", command=self.start_break,
                                            font=("Helvetica", 14), bg="#57c7e3", fg="white", width=15)
        self.start_break_button.grid(row=0, column=1, padx=5)

        # Reset Timer Button
        self.reset_button = tk.Button(self.root, text="Reset Timer", command=self.reset_timer,
                                      font=("Helvetica", 14), bg="#e7305b", fg="white", width=32)
        self.reset_button.pack(pady=20)

        self.root.mainloop()

    def format_time(self, seconds):
        """
        Helper function to format seconds into MM:SS format.
        """
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def start_work_session(self):
        """
        Start a Pomodoro work session.
        """
        if not self.timer_running:
            self.timer_running = True
            self.update_timer(self.work_time, "Work session ended. Time for a break!")

    def start_break(self):
        """
        Start a break session.
        """
        if not self.timer_running:
            self.timer_running = True
            self.update_timer(self.break_time, "Break ended. Back to work!")

    def update_timer(self, remaining_time, end_message):
        """
        Update the timer every second. If time runs out, display the message.
        """
        if remaining_time > 0:
            self.time_label.config(text=self.format_time(remaining_time))
            self.root.after(1000, self.update_timer, remaining_time - 1, end_message)
        else:
            self.timer_running = False
            messagebox.showinfo("Pomodoro Timer", end_message)
            self.reset_timer()

    def reset_timer(self):
        """
        Reset the timer to the default values.
        """
        self.timer_running = False
        self.time_label.config(text=self.format_time(self.work_time))

# Uncomment the line below to create and run the Pomodoro Timer
# pomodoro_timer = PomodoroTimer()
