# main.py
import tkinter as tk
from menu import MainMenu
from db import init_db
init_db()
def run_app():
    root = tk.Tk()
    root.title("Pomodoro Productivity App")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")  # Orqa fon rangi
    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
