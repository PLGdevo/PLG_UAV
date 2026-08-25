import tkinter as tk
from .Styles import Colors


class MapContainer:
    """UI container for the RIGEL MAP_INTERFACE."""

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Colors.CARD)
        self.mounted_widget = None

        toolbar = tk.Frame(self.frame, bg=Colors.CARD)
        toolbar.pack(fill="x", padx=10, pady=6)

        tk.Label(
            toolbar,
            text="BẢN ĐỒ ĐỊA HÌNH & NỀN VỆ TINH",
            font=("Segoe UI", 11, "bold"),
            fg=Colors.CYAN,
            bg=Colors.CARD,
        ).pack(side="left")

        # Map controls: + / - / Home / Center UAV.
        controls = tk.Frame(toolbar, bg=Colors.CARD)
        controls.pack(side="right")

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 3,
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "bg": "#26313d",
            "fg": "white",
            "activebackground": "#344454",
            "activeforeground": "white",
        }

        self.zoom_in_button = tk.Button(
            controls, text="+", command=self.zoom_in, **button_style
        )
        self.zoom_in_button.pack(side="left", padx=2)

        self.zoom_out_button = tk.Button(
            controls, text="−", command=self.zoom_out, **button_style
        )
        self.zoom_out_button.pack(side="left", padx=2)

        self.home_button = tk.Button(
            controls, text="⌂", command=self.go_home, **button_style
        )
        self.home_button.pack(side="left", padx=2)

        self.center_button = tk.Button(
            controls, text="◎", command=self.center_uav, **button_style
        )
        self.center_button.pack(side="left", padx=2)

        self.provider_label = tk.Label(
            toolbar,
            text="MAP INTERFACE: NOT CONNECTED",
            font=("Segoe UI", 8, "bold"),
            fg=Colors.TEXT,
            bg=Colors.CARD,
        )
        self.provider_label.pack(side="right", padx=(10, 8))

        self.host = tk.Frame(
            self.frame,
            bg="#121820",
            bd=1,
            relief="solid",
        )
        self.host.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8),
        )

        self.placeholder_title = tk.Label(
            self.host,
            text="MAP INTERFACE",
            font=("Segoe UI", 18, "bold"),
            fg=Colors.CYAN,
            bg="#121820",
        )
        self.placeholder_title.place(relx=0.5, rely=0.45, anchor="center")

        self.placeholder_text = tk.Label(
            self.host,
            text="Vùng này dành riêng để nhúng Map Interface",
            font=("Segoe UI", 10),
            fg=Colors.TEXT,
            bg="#121820",
        )
        self.placeholder_text.place(relx=0.5, rely=0.53, anchor="center")

    def mount(self, widget):
        """Mount MapWidget without destroying the widget itself."""
        if self.placeholder_title.winfo_exists():
            self.placeholder_title.destroy()
        if self.placeholder_text.winfo_exists():
            self.placeholder_text.destroy()

        if self.mounted_widget is not None and self.mounted_widget != widget:
            try:
                if self.mounted_widget.winfo_exists():
                    self.mounted_widget.destroy()
            except tk.TclError:
                pass

        self.mounted_widget = widget
        widget.pack(fill="both", expand=True)
        self.provider_label.config(text="MAP INTERFACE: READY")

    def _map_call(self, method_name, *args):
        if self.mounted_widget is None:
            return
        try:
            if self.mounted_widget.winfo_exists():
                getattr(self.mounted_widget, method_name)(*args)
        except (tk.TclError, AttributeError):
            pass

    def zoom_in(self):
        self._map_call("zoom_in")

    def zoom_out(self):
        self._map_call("zoom_out")

    def go_home(self):
        self._map_call("go_home")

    def center_uav(self):
        # UAV telemetry will provide the real lat/lon later.
        # Until then, Home view is used as a safe fallback.
        self._map_call("go_home")

    def set_provider_status(self, text):
        self.provider_label.config(text=text)
