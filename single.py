# single.py
import tkinter as tk
from tkinter import font
import threading
import time
import winsound
import os
import sys

class SingleTimerWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.timer_running = False
        self.remaining_time = 25 * 60  # Default: 25 daqiqa
        self.timer_thread = None

        self.create_interface()

    def create_interface(self):
        self.clear_window()

        title = tk.Label(self.master, text="Single Pomodoro Timer", font=self.custom_font)
        title.pack(pady=20)

        self.timer_label = tk.Label(self.master, text="25:00", font=self.custom_font)
        self.timer_label.pack(pady=10)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start", font=self.custom_font, command=self.start_timer).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Stop", font=self.custom_font, command=self.stop_timer).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset", font=self.custom_font, command=self.reset_timer).grid(row=0, column=2, padx=5)

        tk.Button(self.master, text="Bosh Menyuga", font=self.custom_font, command=self.go_back).pack(pady=20)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_timer(self):
        if self.timer_running:
            return

        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        while self.remaining_time > 0 and self.timer_running:
            time.sleep(1)
            self.remaining_time -= 1
            self.master.after(0, self.update_timer)

        if self.timer_running:
            self.timer_running = False
            self.master.after(0, self.play_ringtone)
            self.master.after(0, lambda: self.timer_label.config(text="25:00"))

    def update_timer(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.remaining_time = 25 * 60
        self.timer_label.config(text="25:00")

    def play_ringtone(self):
        try:
            if getattr(sys, 'frozen', False):
                # .exe distributivda ishlayapti
                base_path = os.path.dirname(sys.executable)
            else:
                # Terminalda ishlayapti
                base_path = os.path.dirname(__file__)

            sound_path = os.path.join(base_path, "ring.wav")
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print("🔕 Rington chalib bo‘lmadi:", e)

    def go_back(self):
        self.master.destroy()
