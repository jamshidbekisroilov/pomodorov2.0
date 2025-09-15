import tkinter as tk
from tkinter import font
from db import get_completed_tasks

class CompletedTasksWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.create_interface()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_interface(self):
        self.clear_window()

        title = tk.Label(self.master, text="Bajarilgan Tasklar", font=self.custom_font)
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

        # Jadval sarlavhalari
        headers = ["Sana", "Task nomi", "Pomidor soni"]
        for col, header in enumerate(headers):
            lbl = tk.Label(scroll_frame, text=header, font=self.custom_font, borderwidth=1, relief="solid", width=20)
            lbl.grid(row=0, column=col)

        # Ma’lumotlar
        tasks = get_completed_tasks()
        for row, task in enumerate(tasks, start=1):
            date, name, count = task[1], task[0], task[2]
            tk.Label(scroll_frame, text=date, font=self.custom_font, borderwidth=1, relief="solid", width=20).grid(row=row, column=0)
            tk.Label(scroll_frame, text=name, font=self.custom_font, borderwidth=1, relief="solid", width=20).grid(row=row, column=1)
            tk.Label(scroll_frame, text=str(count), font=self.custom_font, borderwidth=1, relief="solid", width=20).grid(row=row, column=2)

        # Orqaga tugmasi
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Bosh Menyuga", font=self.custom_font, command=self.go_back).pack()

    def go_back(self):
        self.master.destroy()
