# weekly_tasks.py
import tkinter as tk
from tkinter import font, messagebox
from datetime import datetime, timedelta
from db import save_weekly_task, get_all_weekly_tasks

class WeeklyTasksWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        self.tasks = []
        self.create_main_menu()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()

        title = tk.Label(self.master, text="Haftalik Tasklar", font=self.custom_font)
        title.pack(pady=20)

        create_btn = tk.Button(self.master, text="Create Weekly Tasks", font=self.custom_font, command=self.create_task_table)
        create_btn.pack(pady=10)

        see_btn = tk.Button(self.master, text="See Weekly Tasks", font=self.custom_font, command=self.show_saved_tasks)
        see_btn.pack(pady=10)

        back_btn = tk.Button(self.master, text="Bosh Menyuga", font=self.custom_font, command=self.go_back)
        back_btn.pack(pady=30)

    def create_task_table(self):
        self.clear_window()

        title = tk.Label(self.master, text="Yangi Tasklar Jadvali", font=self.custom_font)
        title.pack(pady=10)

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack()

        self.entries = {}  # {(row, day): entry}
        self.task_name_entries = []
        self.task_rows = 1

        self.render_table()

        tk.Button(self.master, text="Add Task", font=self.custom_font, command=self.add_task_row).pack(pady=10)
        tk.Button(self.master, text="Saqlash", font=self.custom_font, command=self.save_tasks).pack(pady=10)
        tk.Button(self.master, text="Orqaga", font=self.custom_font, command=self.create_main_menu).pack(pady=10)

    def render_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        today = datetime.today()
        self.day_dates = []
        for i in range(7):
            day_name = self.days[i]
            date_str = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            self.day_dates.append((day_name, date_str))

        for col, (day, date) in enumerate([("Task", "")] + self.day_dates):
            text = f"{day}\n{date}" if day != "Task" else "Task"
            lbl = tk.Label(self.table_frame, text=text, font=self.custom_font, borderwidth=1, relief="solid", width=14)
            lbl.grid(row=0, column=col)

        self.task_name_entries.clear()
        for row in range(1, self.task_rows + 1):
            name_entry = tk.Entry(self.table_frame, font=self.custom_font, width=14)
            name_entry.grid(row=row, column=0)
            self.task_name_entries.append(name_entry)

            for col, (day, date) in enumerate(self.day_dates, start=1):
                entry = tk.Entry(self.table_frame, font=self.custom_font, width=5, justify="center")
                entry.grid(row=row, column=col)
                self.entries[(row, day)] = entry

    def add_task_row(self):
        self.task_rows += 1
        self.render_table()

    def save_tasks(self):
        self.tasks.clear()
        for row in range(1, self.task_rows + 1):
            task_name = self.task_name_entries[row - 1].get().strip()
            if not task_name:
                continue
            for day, date in self.day_dates:
                value = self.entries[(row, day)].get()
                if value.isdigit():
                    pomidor_count = int(value)
                    self.tasks.append({
                        "task": task_name,
                        "day": day,
                        "date": date,
                        "pomidor": pomidor_count
                    })
                    save_weekly_task(task_name, day, date, pomidor_count)

        messagebox.showinfo("Saqlash", "Tasklar bazaga saqlandi!")

    def show_saved_tasks(self):
        self.clear_window()
        title = tk.Label(self.master, text="Saqlangan Tasklar", font=self.custom_font)
        title.pack(pady=10)

        # 🔄 Scrollable frame yaratamiz
        canvas = tk.Canvas(self.master, height=400)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 🔽 Tasklarni scroll_frame ichida ko‘rsatamiz
        tasks = get_all_weekly_tasks()
        for i, task in enumerate(tasks):
            task_name, day, date, pomidor = task
            row_text = f"{task_name} — {day} ({date}) : {pomidor} pomidor"
            lbl = tk.Label(scroll_frame, text=row_text, font=self.custom_font)
            lbl.grid(row=i, column=0, pady=2, sticky="w")

        # 🔙 Tugmalar pastda
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Tahrirlash", font=self.custom_font, command=self.create_task_table).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Orqaga", font=self.custom_font, command=self.create_main_menu).pack(side="left", padx=10)

    def go_back(self):
        self.master.destroy()  # Yangi oynani yopadi

