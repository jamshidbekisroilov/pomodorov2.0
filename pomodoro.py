import tkinter as tk
from tkinter import font, messagebox
from datetime import datetime
import threading
import time
import os
import sys
import winsound
from db import get_today_weekly_tasks, save_completed_task, save_single_task, get_connection

class PomodoroWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.timer_running = False
        self.break_mode = False
        self.long_break_counter = 0
        self.remaining_time = 0
        self.selected_task = None
        self.timer_thread = None

        self.create_interface()

    def create_interface(self):
        self.clear_window()

        title = tk.Label(self.master, text="Pomodoro Timer", font=self.custom_font)
        title.pack(pady=20)

        # Bugungi tasklar ro‘yxati
        today = datetime.today().strftime("%Y-%m-%d")
        self.task_list = get_today_weekly_tasks(today)
        task_names = [task[0] for task in self.task_list]

        self.task_var = tk.StringVar()
        if task_names:
            self.task_var.set(task_names[0])
        else:
            task_names = ["No tasks"]
            self.task_var.set("No tasks")

        self.task_menu = tk.OptionMenu(self.master, self.task_var, *task_names)
        self.task_menu.config(font=self.custom_font, width=25)
        self.task_menu.pack(pady=10)

        # Timer ko‘rsatkich
        self.timer_label = tk.Label(self.master, text="25:00", font=self.custom_font)
        self.timer_label.pack(pady=10)

        # Tugmalar
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start", font=self.custom_font, command=self.start_timer).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Stop", font=self.custom_font, command=self.stop_timer).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset", font=self.custom_font, command=self.reset_timer).grid(row=0, column=2, padx=5)

        # Birmartalik task qo‘shish
        tk.Button(self.master, text="Add New Task", font=self.custom_font, command=self.add_single_task).pack(pady=10)

        # Orqaga
        tk.Button(self.master, text="Bosh Menyuga", font=self.custom_font, command=self.go_back).pack(pady=20)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_timer(self):
        if self.timer_running:
            return

        self.selected_task = self.task_var.get()
        if not self.selected_task or self.selected_task == "No tasks":
            messagebox.showwarning("Diqqat", "Iltimos, taskni tanlang.")
            return

        self.timer_running = True
        self.remaining_time = 25 * 60 if not self.break_mode else (15 * 60 if self.long_break_counter == 3 else 5 * 60)
        self.update_timer()

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

            if not self.break_mode:
                today = datetime.today().strftime("%Y-%m-%d")
                save_completed_task(self.selected_task, today)
                self.long_break_counter += 1
                self.break_mode = True
                self.master.after(0, lambda: messagebox.showinfo("Tanaffus", "Pomodoro tugadi! Endi dam olish vaqti."))
            else:
                self.break_mode = False
                if self.long_break_counter == 3:
                    self.long_break_counter = 0
                self.master.after(0, lambda: messagebox.showinfo("Davom etamiz", "Dam tugadi! Yana Pomodoro boshlaymiz."))

            self.master.after(0, self.update_timer)

    def update_timer(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.remaining_time = 0
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


    def add_single_task(self):
        today = datetime.today().strftime("%Y-%m-%d")
        task_name = f"SingleTask-{int(time.time())}"
        save_single_task(task_name, today)
        messagebox.showinfo("Qo‘shildi", f"Yangi task qo‘shildi: {task_name}")
    

    def go_back(self):
        self.master.destroy()  # Yangi oynani yopadi

