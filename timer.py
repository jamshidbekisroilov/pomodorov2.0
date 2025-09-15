# timer.py
import threading
import time

class PomodoroTimer:
    def __init__(self, duration_seconds, on_tick, on_finish):
        self.duration = duration_seconds
        self.remaining = duration_seconds
        self.on_tick = on_tick          # Har soniyada chaqiriladi
        self.on_finish = on_finish      # Tugaganda chaqiriladi
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self.remaining > 0 and self.running:
            time.sleep(1)
            self.remaining -= 1
            self.on_tick(self.remaining)

        if self.running:
            self.running = False
            self.on_finish()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.remaining = self.duration
        self.on_tick(self.remaining)

    def is_running(self):
        return self.running
