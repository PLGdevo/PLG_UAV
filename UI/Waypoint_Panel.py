import tkinter as tk
from tkinter import ttk
from .Styles import Colors, button


class WaypointPanel:
    """
    UI chỉ hiển thị/chỉnh sửa danh sách waypoint.
    Dữ liệu waypoint thực tế sau này lấy từ MAP_INTERFACE.
    """

    def __init__(self, parent, on_delete=None, on_clear=None, on_select=None):
        self.on_delete = on_delete or (lambda: None)
        self.on_clear = on_clear or (lambda: None)
        self.on_select = on_select or (lambda index: None)

        self.frame = tk.Frame(parent, bg=Colors.CARD)

        tk.Label(
            self.frame,
            text="DANH SÁCH WAYPOINT",
            font=("Segoe UI", 11, "bold"),
            fg=Colors.CYAN,
            bg=Colors.CARD,
        ).pack(anchor="w", padx=12, pady=8)

        table = tk.Frame(self.frame, bg=Colors.CARD)
        table.pack(fill="x", padx=10)

        self.tree = ttk.Treeview(
            table,
            columns=("id", "lat", "lon", "alt", "speed"),
            show="headings",
            height=8,
            style="Rigel.Treeview",
        )

        headers = {
            "id": "WP",
            "lat": "LAT",
            "lon": "LON",
            "alt": "ALT",
            "speed": "SPD",
        }

        widths = {
            "id": 42,
            "lat": 68,
            "lon": 68,
            "alt": 55,
            "speed": 55,
        }

        for col in headers:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._select)

        buttons = tk.Frame(self.frame, bg=Colors.CARD)
        buttons.pack(fill="x", padx=10, pady=5)

        button(
            buttons,
            "❌ Xóa Điểm Chọn",
            self.on_delete,
            "#c62828",
            pady=5,
        ).pack(side="left", fill="x", expand=True, padx=(0, 2))

        button(
            buttons,
            "🗑️ Xóa Tất Cả",
            self.on_clear,
            "#37474f",
            pady=5,
        ).pack(side="right", fill="x", expand=True, padx=(2, 0))

    def _select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        self.on_select(self.tree.index(selected[0]))

    def set_waypoints(self, waypoints, selected_index=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, wp in enumerate(waypoints):
            self.tree.insert(
                "",
                "end",
                values=(
                    wp.get("id", f"WP{i+1}"),
                    f"{wp.get('lat', 0):.6f}",
                    f"{wp.get('lon', 0):.6f}",
                    f"{wp.get('alt', 0):.1f}",
                    f"{wp.get('speed', 0):.1f}",
                ),
            )

        if selected_index is not None and 0 <= selected_index < len(waypoints):
            items = self.tree.get_children()
            self.tree.selection_set(items[selected_index])
