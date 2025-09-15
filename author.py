# author.py
import tkinter as tk
from tkinter import font

class AuthorWindow:
    def __init__(self, master):
        self.master = master
        self.custom_font = font.Font(family="Arial", size=16, weight="bold")
        self.create_interface()

    def create_interface(self):
        self.clear_window()

        title = tk.Label(self.master, text="Muallif Haqida", font=self.custom_font)
        title.pack(pady=20)

        info_text = (
            "👨‍💻 Jamshidbek Isroilov\n"
            "Python dasturchi Vibe coder.\n"
            "Modular desktop, web va bot ilovalar yaratadi.\n"
            "Vibe Coding orqali amaliy mini-kurslar taqdim etadi.\n\n"
            "📚 Maqsadi: Texnologiyani o‘zbek tilida tushunarli va amaliy o‘rgatish.\n"
            "🎯 Pomodoro ilovasi — samaradorlikni oshirish uchun yaratilgan.\n\n"
            "🌐 Ijtimoiy sahifalar:\n"
            "Aloqa:t.me/jamshidbekisroilov2000\n"
            "GitHub: https://github.com/jamshidbekisroilov\n"
            "LinkedIn: https://www.linkedin.com/in/jamshidbek-isroilov-accountant\n"
            "Telegram: https://t.me/jamshidbekisroilov2000\n"
            "Email:jisroilov45@gamil.com\n"
            "Website: https://portfolio-site-cals.onrender.com"
        )

        text_box = tk.Text(self.master, font=self.custom_font, width=70, height=15, wrap="word")
        text_box.pack(padx=20)
        text_box.insert(tk.END, info_text)
        text_box.config(state="disabled")

        tk.Button(self.master, text="Bosh Menyuga", font=self.custom_font, command=self.go_back).pack(pady=20)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.master.destroy()  # Yangi oynani yopadi


