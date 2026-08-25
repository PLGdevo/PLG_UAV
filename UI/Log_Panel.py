import time
import tkinter as tk
from .Styles import Colors


class LogPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Colors.CARD)

        tk.Label(
            self.frame,
            text="NHẬT KÝ TELEMETRY / HỆ THỐNG",
            font=("Segoe UI", 9, "bold"),
            fg=Colors.TEXT,
            bg=Colors.CARD,
        ).pack(anchor="w", padx=12, pady=(8, 2))

        self.text = tk.Text(
            self.frame,
            bg="#101419",
            fg=Colors.CYAN,
            font=("Consolas", 8),
            bd=1,
            relief="solid",
            height=7,
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=(2, 8))

    def write(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.text.insert("end", f"[{timestamp}] {message}\n")
        self.text.see("end")
