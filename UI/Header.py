import tkinter as tk
from .Styles import Colors


class Header:
    def __init__(self, parent):
        self.frame = tk.Frame(
            parent,
            bg=Colors.PANEL,
            height=52,
            bd=1,
            relief="solid",
        )
        self.frame.pack(fill="x", side="top")
        self.frame.pack_propagate(False)

        self._build()

    def _build(self):
        left = tk.Frame(self.frame, bg=Colors.PANEL)
        left.pack(side="left", padx=15)

        tk.Label(
            left,
            text="🚁 RIGEL GCS",
            font=("Segoe UI", 14, "bold"),
            fg=Colors.CYAN,
            bg=Colors.PANEL,
        ).pack(side="left")

        tk.Label(
            left,
            text="v1.0 | Trạm Điều Khiển Bay Mặt Đất Tự Động",
            font=("Segoe UI", 10),
            fg=Colors.TEXT,
            bg=Colors.PANEL,
        ).pack(side="left", padx=10)

        right = tk.Frame(self.frame, bg=Colors.PANEL)
        right.pack(side="right", padx=15)

        self.mode = tk.Label(
            right,
            text="[ DISARMED ]",
            font=("Segoe UI", 10, "bold"),
            fg=Colors.WHITE,
            bg="#37474f",
            padx=10,
            pady=4,
        )
        self.mode.pack(side="left", padx=5)

        self.telemetry = tk.Label(
            right,
            text="● TELEMETRY ONLINE",
            font=("Segoe UI", 9, "bold"),
            fg=Colors.GREEN,
            bg=Colors.PANEL,
        )
        self.telemetry.pack(side="left", padx=10)

        self.gcs = tk.Label(
            right,
            text="GCS: READY",
            font=("Segoe UI", 9, "bold"),
            fg=Colors.CYAN,
            bg=Colors.PANEL,
        )
        self.gcs.pack(side="left")

    def set_mode(self, mode):
        self.mode.config(text=f"[ {mode} ]")

    def set_telemetry(self, online):
        self.telemetry.config(
            text="● TELEMETRY ONLINE" if online else "● TELEMETRY OFFLINE",
            fg=Colors.GREEN if online else Colors.RED,
        )

    def set_gcs_status(self, status):
        self.gcs.config(text=f"GCS: {status}")
