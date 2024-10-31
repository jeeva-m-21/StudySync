import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END
import pyaudio
import wave
import threading
import mysql.connector
import os

class AudioRecorder:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Audio Recorder")
        self.root.configure(bg='lightblue')  # Set the background color

        # Record button with visible text
        self.record_button = tk.Button(self.root, text="Record", command=self.start_recording, bg='blue', fg='white', font=('Arial', 12, 'bold'))
        self.record_button.pack(pady=10)

        # Stop button with visible text
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording, state=tk.DISABLED, bg='red', fg='white', font=('Arial', 12, 'bold'))
        self.stop_button.pack(pady=10)

        # Play button with visible text
        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio, state=tk.DISABLED, bg='green', fg='white', font=('Arial', 12, 'bold'))
        self.play_button.pack(pady=10)

        self.previous_recordings_label = tk.Label(self.root, text="Previous Recordings:", bg='lightblue', fg='darkblue', font=('Arial', 14, 'bold'))
        self.previous_recordings_label.pack(pady=5)

        # Listbox for previous recordings with visible text
        self.recordings_listbox = Listbox(self.root, width=50, bg='white', fg='black', selectbackground='lightgrey', font=('Arial', 12))
        self.recordings_listbox.pack(pady=5)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recordings_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.recordings_listbox.yview)

        self.recordings_listbox.bind("<<ListboxSelect>>", self.on_select)

        self.is_recording = False
        self.audio_file = "recorded_audio.wav"

        self.db_connection = self.connect_to_database()
        self.load_previous_recordings()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Smks1_1030",  # Replace with your password
                database="study_sync_db"
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.record).start()

    def record(self):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100

        audio = pyaudio.PyAudio()
        stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

        frames = []
        while self.is_recording:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.audio_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.record_button.config(state=tk.NORMAL)

        self.save_to_database(self.audio_file)
        messagebox.showinfo("Info", "Recording saved successfully!")
        self.load_previous_recordings()

    def stop_recording(self):
        self.is_recording = False

    def play_audio(self):
        selected_file = self.recordings_listbox.get(self.recordings_listbox.curselection())
        self.play_audio_file(selected_file)

    def play_audio_file(self, file_path):
        chunk = 1024
        wf = wave.open(file_path, 'rb')
        audio = pyaudio.PyAudio()

        stream = audio.open(format=pyaudio.paInt16,
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        messagebox.showinfo("Info", "Playback finished.")

    def save_to_database(self, file_path):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO recordings (username, file_path) VALUES (%s, %s)"
        values = (self.username, file_path)
        try:
            cursor.execute(query, values)
            self.db_connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def load_previous_recordings(self):
        self.recordings_listbox.delete(0, END)  # Clear the listbox
        cursor = self.db_connection.cursor()
        query = "SELECT file_path FROM recordings WHERE username = %s"
        cursor.execute(query, (self.username,))
        recordings = cursor.fetchall()

        for recording in recordings:
            file_path = recording[0]
            if os.path.exists(file_path):
                self.recordings_listbox.insert(END, file_path)

        cursor.close()

    def on_select(self, event):
        if self.recordings_listbox.curselection():
            self.play_button.config(state=tk.NORMAL)  # Enable the play button if a recording is selected
        else:
            self.play_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

def recordrunner(username):
    app = AudioRecorder(username)
    app.run()







