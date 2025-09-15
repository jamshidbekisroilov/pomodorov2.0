# menu.py
import tkinter as tk
from tkinter import font
from weekly_tasks import WeeklyTasksWindow
from pomodoro import PomodoroWindow
from completed_tasks import CompletedTasksWindow
from analysis import AnalysisWindow
from author import AuthorWindow
from single import SingleTimerWindow
class MainMenu:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.master, text="Pomodoro Productivity App", font=self.custom_font, bg="#f0f0f0")
        title.pack(pady=30)

        buttons = [
            ("Pomodoro Timer", self.open_pomodoro),
            ("Haftalik Tasklar", self.open_weekly_tasks),
            ("Bajarilgan Tasklar", self.open_completed_tasks),
            ("Tahlil", self.open_analysis),
            ("Muallif", self.open_author),
            ("Single Timer", self.open_single_timer)
        ]

        for text, command in buttons:
            btn = tk.Button(self.master, text=text, font=self.custom_font, width=25, height=2, command=command)
            btn.pack(pady=10)

    def open_pomodoro(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Pomodoro Timer")
        new_window.geometry("800x600")
        PomodoroWindow(new_window)

    def open_weekly_tasks(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Haftalik Tasklar")
        new_window.geometry("1000x600")
        WeeklyTasksWindow(new_window)

    def open_completed_tasks(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Bajarilgan Tasklar")
        new_window.geometry("800x600")
        CompletedTasksWindow(new_window)

    def open_analysis(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Tahlil")
        new_window.geometry("800x600")
        AnalysisWindow(new_window)

    def open_author(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Muallif")
        new_window.geometry("800x600")
        AuthorWindow(new_window)
    from single import SingleTimerWindow

    def open_single_timer(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Single Timer")
        new_window.geometry("800x600")
        SingleTimerWindow(new_window)
