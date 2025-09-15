# analysis.py
import tkinter as tk
from tkinter import font
from db import get_task_statistics
import matplotlib.pyplot as plt

class AnalysisWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.create_interface()

    def create_interface(self):
        self.clear_window()

        title = tk.Label(self.master, text="Statistik Tahlil", font=self.custom_font)
        title.pack(pady=20)

        tk.Button(self.master, text="Bajarilgan Tasklar Diagrammasi", font=self.custom_font, command=self.show_completed_chart).pack(pady=10)
        tk.Button(self.master, text="Bajarilmagan Tasklar Diagrammasi", font=self.custom_font, command=self.show_uncompleted_chart).pack(pady=10)
        tk.Button(self.master, text="Umumiy Statistikalar", font=self.custom_font, command=self.show_summary).pack(pady=10)

        tk.Button(self.master, text="Bosh Menyuga", font=self.custom_font, command=self.go_back).pack(pady=30)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_completed_chart(self):
        stats = get_task_statistics()
        data = stats["completed"]

        if not data:
            self.show_message("Bajarilgan tasklar topilmadi.")
            return

        labels = [item[0] for item in data]
        sizes = [item[1] for item in data]

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Bajarilgan Tasklar Ulushi")
        plt.show()

    def show_uncompleted_chart(self):
        stats = get_task_statistics()
        completed = {item[0]: item[1] for item in stats["completed"]}
        planned = {item[0]: item[1] for item in stats["planned"]}

        uncompleted = {}
        for task, plan_count in planned.items():
            done_count = completed.get(task, 0)
            if plan_count > done_count:
                uncompleted[task] = plan_count - done_count

        if not uncompleted:
            self.show_message("Bajarilmagan tasklar topilmadi.")
            return

        labels = list(uncompleted.keys())
        sizes = list(uncompleted.values())

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Bajarilmagan Tasklar Ulushi")
        plt.show()

    def show_summary(self):
        stats = get_task_statistics()
        completed = stats["completed"]
        planned = stats["planned"]

        summary_text = "📊 Umumiy Statistikalar:\n\n"
        for task, plan_count in planned:
            done_count = next((c for t, c in completed if t == task), 0)
            summary_text += f"{task}: Rejalangan {plan_count} ta, Bajarilgan {done_count} ta\n"

        self.clear_window()
        tk.Label(self.master, text="Umumiy Statistikalar", font=self.custom_font).pack(pady=10)

        text_box = tk.Text(self.master, font=self.custom_font, width=60, height=15)
        text_box.pack()
        text_box.insert(tk.END, summary_text)
        text_box.config(state="disabled")

        tk.Button(self.master, text="Orqaga", font=self.custom_font, command=self.create_interface).pack(pady=20)

    def show_message(self, msg):
        tk.messagebox.showinfo("Ma’lumot", msg)

    def go_back(self):
        self.master.destroy()  # Yangi oynani yopadi

