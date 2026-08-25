import math
import threading
import tkinter as tk
from pymavlink import mavutil
from .Styles import Colors


class FlightHUD:
    """
    UI HUD 3D - Tối ưu hiệu năng 60 FPS, chống chớp/flicker màn hình.
    """

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Colors.CARD)

        tk.Label(
            self.frame,
            text="GIÁM SÁT BAY & HUD 3D",
            font=("Segoe UI", 11, "bold"),
            fg=Colors.CYAN,
            bg=Colors.CARD,
        ).pack(anchor="w", padx=12, pady=8)

        # Kích thước cố định ban đầu
        self.w = 296
        self.h = 300
        self.cx = self.w / 2
        self.cy = 125

        self.canvas = tk.Canvas(
            self.frame,
            bg="#11161d",
            width=self.w,
            height=self.h,
            highlightthickness=1,
            highlightbackground=Colors.BORDER,
        )
        self.canvas.pack(fill="x", padx=10)

        values = tk.Frame(self.frame, bg=Colors.CARD)
        values.pack(fill="x", padx=10, pady=6)

        self.alt = self._value(values, "ĐỘ CAO: 0.0 m", Colors.GREEN, 0, 0)
        self.speed = self._value(values, "TỐC ĐỘ: 0.0 km/h", Colors.CYAN, 0, 1)
        self.heading = self._value(values, "HƯỚNG: 000°", Colors.AMBER, 1, 0, 2)

        self.altitude = 0.0
        self.speed_value = 0.0
        self.heading_value = 0.0
        self.pitch = 0.0
        self.roll = 0.0

        values.grid_columnconfigure(0, weight=1)
        values.grid_columnconfigure(1, weight=1)

        # VẼ KHUNG CỐ ĐỊNH TRÊN CANVAS 1 LẦN DUY NHẤT
        self._init_canvas_items()
        self.draw()

    def _value(self, parent, text, fg, row, col, span=1):
        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            fg=fg,
            bg=Colors.CARD,
        )
        label.grid(
            row=row,
            column=col,
            columnspan=span,
            sticky="w" if col == 0 else "e",
            pady=2,
        )
        return label

    def _init_canvas_items(self):
        """Tạo các đối tượng trên Canvas một lần duy nhất để chỉ việc update tọa độ"""
        c = self.canvas
        w, h, cx, cy = self.w, self.h, self.cx, self.cy

        # 1. Sky (Bầu trời)
        self.sky_id = c.create_rectangle(8, 8, w - 8, h - 55, fill="#1976d2", outline="")

        # 2. Ground (Mặt đất)
        self.ground_id = c.create_rectangle(8, cy, w - 8, h - 55, fill="#5d4037", outline="")

        # 3. Horizon Line (Đường chân trời)
        self.horizon_id = c.create_line(cx - 125, cy, cx + 125, cy, fill=Colors.WHITE, width=2)

        # 4. Aircraft Symbol (Biểu tượng máy bay cố định ở trung tâm)
        c.create_line(cx - 35, cy, cx - 10, cy, fill=Colors.AMBER, width=4)
        c.create_line(cx + 10, cy, cx + 35, cy, fill=Colors.AMBER, width=4)
        c.create_line(cx, cy - 10, cx, cy + 10, fill=Colors.AMBER, width=3)
        c.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, outline=Colors.AMBER, width=2)

        # Title Text
        c.create_text(
            cx, 20,
            text="ARTIFICIAL HORIZON",
            fill=Colors.WHITE,
            font=("Segoe UI", 8, "bold"),
        )

        # 5. Compass Box & Text
        c.create_rectangle(
            8, h - 48, w - 8, h - 8,
            fill=Colors.PANEL,
            outline=Colors.BORDER,
        )
        self.compass_text_id = c.create_text(
            cx, h - 39,
            text="COMPASS  0°",
            fill=Colors.CYAN,
            font=("Segoe UI", 8, "bold"),
        )

    def update(self, altitude, speed, heading, pitch=0.0, roll=0.0):
        self.altitude = altitude
        self.speed_value = speed
        self.heading_value = heading
        self.pitch = pitch
        self.roll = roll

        self.alt.config(text=f"ĐỘ CAO: {altitude:.1f} m")
        self.speed.config(text=f"TỐC ĐỘ: {speed:.1f} km/h")
        self.heading.config(text=f"HƯỚNG: {heading % 360:.0f}°")

        self.draw()

    def draw(self):
        c = self.canvas
        
        # Lấy chiều rộng an toàn (tránh trường hợp winfo_width() = 1 khi chưa render)
        actual_w = c.winfo_width()
        w = actual_w if actual_w > 10 else self.w
        h = self.h
        cx = w / 2
        cy = 125

        # Giới hạn góc Pitch không vượt quá khung nhìn HUD
        pitch_y = cy + self.pitch * 3
        pitch_y = max(8, min(h - 55, pitch_y))

        # 1. Cập nhật vị trí Mặt đất (Ground)
        c.coords(self.ground_id, 8, pitch_y, w - 8, h - 55)

        # 2. Cập nhật Đường chân trời xoay theo Roll
        angle = math.radians(self.roll)
        dx = math.cos(angle) * 125
        dy = math.sin(angle) * 125
        c.coords(self.horizon_id, cx - dx, pitch_y - dy, cx + dx, pitch_y + dy)

        # 3. Cập nhật Text La bàn
        c.itemconfigure(self.compass_text_id, text=f"COMPASS  {self.heading_value % 360:.0f}°")
        c.coords(self.compass_text_id, cx, h - 39)