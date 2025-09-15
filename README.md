 🕒 Pomodoro Productivity App

Bu Python asosida yaratilgan desktop ilova sizga Pomodoro texnikasi orqali haftalik tasklaringizni rejalashtirish, bajarilgan ishlarni kuzatish va o‘z faoliyatingizni tahlil qilish imkonini beradi.

## ✨ Asosiy imkoniyatlar

- ⏱️ Pomodoro timer (25 daqiqa ish, 5/15 daqiqa dam)
- 📅 Haftalik tasklar jadvali (kunlik pomidorlar bilan)
- ✅ Bajarilgan tasklar ro‘yxati
- 📊 Statistik tahlil (rejalashtirilgan vs bajarilgan)
- 🔔 Rington chalish (ring.wav)
- 🧪 Test rejimi (10 soniya Pomodoro)
- 📈 Diagramma yasash (matplotlib bilan)

## 📦 O‘rnatish

```bash
pip install -r requirements.txt
Yoki .exe distributivni yuklab oling va main.exe faylni ishga tushiring.

🛠️ Texnologiyalar
Python 3.10+

Tkinter (GUI)

SQLite (ma’lumotlar bazasi)

PyInstaller (distributiv)

winsound (rington)

matplotlib (diagramma)

📁 Fayl tuzilmasi
Код
pomodoro/
├── main.py
├── menu.py
├── pomodoro.py
├── weekly_tasks.py
├── completed_tasks.py
├── analysis.py
├── single.py
├── diagram.py
├── db.py
├── ring.wav
└── pomodoro.db
📥 Distributiv yaratish
bash
pyinstaller --onefile --noconsole --add-data "ring.wav;." main.py
👨‍💻 Muallif
Jamshidbek Isroilov Python developer & educator
