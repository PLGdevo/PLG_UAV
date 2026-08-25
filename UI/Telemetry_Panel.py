import tkinter as tk
from .Styles import Colors


class TelemetryPanel:
    def __init__(self, parent):
        self.frame = tk.LabelFrame(
            parent,
            text=" TRẠNG THÁI HỆ THỐNG ",
            font=("Segoe UI", 9, "bold"),
            fg=Colors.TEXT,
            bg=Colors.CARD,
            bd=1,
        )
        self.frame.pack(fill="x", padx=10, pady=10, ipady=5)

        self.battery = self._label("🔋 PIN: --", Colors.GREEN)
        self.gps = self._label("🛰️ VỆ TINH GPS: --", Colors.WHITE)
        self.telemetry = self._label("📶 SÓNG TELEMETRY: --", Colors.CYAN)

    def _label(self, text, fg):
        label = tk.Label(
            self.frame,
            text=text,
            font=("Segoe UI", 9, "bold"),
            fg=fg,
            bg=Colors.CARD,
        )
        label.pack(anchor="w", padx=10, pady=2)
        return label

    def update(
        self,
        battery_pct=None,
        voltage=None,
        satellites=None,
        fix_type=None,
        signal_pct=None,
        signal_dbm=None,
    ):
        if battery_pct is not None:
            voltage_text = f" ({voltage:.1f}V)" if voltage is not None else ""
            self.battery.config(
                text=f"🔋 PIN: {battery_pct:.1f}%{voltage_text}"
            )

        if satellites is not None:
            fix = f" ({fix_type})" if fix_type else ""
            self.gps.config(
                text=f"🛰️ VỆ TINH GPS: {satellites}{fix}"
            )

        if signal_pct is not None:
            dbm = f" ({signal_dbm}dBm)" if signal_dbm is not None else ""
            self.telemetry.config(
                text=f"📶 SÓNG TELEMETRY: {signal_pct:.0f}%{dbm}"
            )
