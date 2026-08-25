import tkinter as tk
from .Styles import Colors, button


class CommandPanel:
    """
    UI command surface.
    Không gửi MAVLink/Protocol trực tiếp.
    Mọi command đi qua callback.
    """

    def __init__(self, parent, on_command=None):
        self.on_command = on_command or (lambda command: None)

        self.frame = tk.Frame(parent, bg=Colors.CARD)

        tk.Label(
            self.frame,
            text="BẢNG LỆNH ĐIỀU KHIỂN (ONE-CLICK)",
            font=("Segoe UI", 10, "bold"),
            fg=Colors.WHITE,
            bg=Colors.CARD,
        ).pack(anchor="w", padx=12, pady=(12, 4))

        box = tk.Frame(self.frame, bg=Colors.CARD)
        box.pack(fill="x", padx=10)

        self.arm = button(
            box,
            "⚡ ARM / KHÓA ĐỘNG CƠ",
            lambda: self.on_command("ARM"),
            "#388e3c",
        )
        self.arm.pack(fill="x", pady=3)

        button(
            box,
            "🛫 CẤT CÁNH (TAKEOFF)",
            lambda: self.on_command("TAKEOFF"),
            Colors.BLUE,
        ).pack(fill="x", pady=3)

        button(
            box,
            "🏠 QUAY VỀ (RTL)",
            lambda: self.on_command("RTL"),
            Colors.PURPLE,
        ).pack(fill="x", pady=3)

        button(
            box,
            "🛬 HẠ CÁNH (LAND)",
            lambda: self.on_command("LAND"),
            Colors.ORANGE,
        ).pack(fill="x", pady=3)

        button(
            box,
            "🛑 DỪNG BAY / TẠM DỪNG",
            lambda: self.on_command("PAUSE"),
            Colors.RED,
        ).pack(fill="x", pady=3)

    def set_armed(self, armed):
        self.arm.config(
            text="🔒 DISARM (TẮT ĐỘNG CƠ)" if armed else "⚡ ARM / KHÓA ĐỘNG CƠ",
            bg="#d32f2f" if armed else "#388e3c",
            activebackground="#d32f2f" if armed else "#388e3c",
        )
