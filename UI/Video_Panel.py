import tkinter as tk
from tkinter import ttk
from .Styles import Colors


class VideoPanel:
    """
    Camera panel cố định trong layout chính.

    - Hiển thị preview camera ở khu vực panel.
    - Có combobox chọn camera.
    - Có nút mở camera lớn hơn.
    - Module camera thật được mount qua `mount()`.
    """

    def __init__(self, parent, on_camera_change=None):
        self.on_camera_change = on_camera_change or (lambda _index: None)
        self.mounted_widget = None
        self.expand_window = None

        self.frame = tk.Frame(
            parent,
            bg=Colors.PANEL,
            height=225,
            bd=1,
            relief="solid",
        )
        self.frame.pack(fill="x", padx=10, pady=(8, 6))
        self.frame.pack_propagate(False)

        # --------------------------------------------------------
        # HEADER / CAMERA CONTROLS
        # --------------------------------------------------------
        header = tk.Frame(self.frame, bg=Colors.PANEL)
        header.pack(fill="x", padx=8, pady=(5, 4))

        tk.Label(
            header,
            text="📷 CAMERA",
            font=("Segoe UI", 9, "bold"),
            fg=Colors.AMBER,
            bg=Colors.PANEL,
        ).pack(side="left")

        self.status = tk.Label(
            header,
            text="NOT CONNECTED",
            font=("Segoe UI", 8, "bold"),
            fg=Colors.TEXT,
            bg=Colors.PANEL,
        )
        self.status.pack(side="right")

        controls = tk.Frame(self.frame, bg=Colors.PANEL)
        controls.pack(fill="x", padx=8, pady=(0, 4))

        tk.Label(
            controls,
            text="Camera:",
            font=("Segoe UI", 8, "bold"),
            fg=Colors.TEXT,
            bg=Colors.PANEL,
        ).pack(side="left")

        self.camera_var = tk.StringVar(value="Camera 0")
        self.camera_box = ttk.Combobox(
            controls,
            textvariable=self.camera_var,
            values=("Camera 0", "Camera 1", "Camera 2", "Camera 3"),
            state="readonly",
            width=12,
        )
        self.camera_box.pack(side="left", padx=(5, 6))
        self.camera_box.bind("<<ComboboxSelected>>", self._camera_selected)

        self.expand_button = tk.Button(
            controls,
            text="⛶ Xem cam lớn",
            command=self.open_large_view,
            font=("Segoe UI", 8, "bold"),
            bd=0,
            relief="flat",
            cursor="hand2",
            bg="#26313d",
            fg="white",
            activebackground="#344454",
            activeforeground="white",
            padx=8,
            pady=3,
        )
        self.expand_button.pack(side="right")

        # --------------------------------------------------------
        # VIDEO HOST
        # --------------------------------------------------------
        self.host = tk.Frame(
            self.frame,
            bg="#080b0e",
            bd=1,
            relief="solid",
        )
        self.host.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.placeholder = tk.Label(
            self.host,
            text="VIDEO MODULE\nChưa kết nối camera",
            justify="center",
            font=("Segoe UI", 10, "bold"),
            fg=Colors.TEXT,
            bg="#080b0e",
        )
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def _camera_selected(self, _event=None):
        selected = self.camera_box.current()
        if selected < 0:
            return
        self.on_camera_change(selected)

    def get_selected_camera_index(self):
        return max(0, self.camera_box.current())

    def set_camera_options(self, options):
        """Đặt danh sách camera hiển thị trong combobox."""
        self.camera_box["values"] = options
        if options:
            self.camera_var.set(options[0])

    def mount(self, widget):
        """Nhúng camera widget vào panel."""
        self.mounted_widget = widget

        if self.placeholder.winfo_exists():
            self.placeholder.destroy()

        widget.pack(fill="both", expand=True)

    def set_status(self, text):
        self.status.config(text=text)

    def open_large_view(self):
        """Mở preview camera trong cửa sổ lớn hơn."""
        if self.expand_window is not None:
            try:
                if self.expand_window.winfo_exists():
                    self.expand_window.lift()
                    self.expand_window.focus_force()
                    return
            except tk.TclError:
                pass

        self.expand_window = tk.Toplevel(self.frame)
        self.expand_window.title("RIGEL - CAMERA VIEW")
        self.expand_window.geometry("900x560")
        self.expand_window.minsize(640, 400)
        self.expand_window.configure(bg=Colors.BG)

        top = tk.Frame(self.expand_window, bg=Colors.PANEL)
        top.pack(fill="x", padx=8, pady=8)

        tk.Label(
            top,
            text=f"📷 {self.camera_var.get()}",
            font=("Segoe UI", 10, "bold"),
            fg=Colors.AMBER,
            bg=Colors.PANEL,
        ).pack(side="left", padx=8, pady=5)

        tk.Button(
            top,
            text="Đóng",
            command=self._close_large_view,
            font=("Segoe UI", 8, "bold"),
            bd=0,
            cursor="hand2",
            bg="#26313d",
            fg="white",
            activebackground="#344454",
            activeforeground="white",
            padx=10,
            pady=4,
        ).pack(side="right", padx=6, pady=3)

        large_host = tk.Frame(
            self.expand_window,
            bg="#080b0e",
            bd=1,
            relief="solid",
        )
        large_host.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Camera widget được tạo lại từ factory nếu module hỗ trợ.
        if self.mounted_widget is not None:
            try:
                camera = self.mounted_widget.__class__(
                    large_host,
                    width=880,
                    height=500,
                )
                camera.pack(fill="both", expand=True)
                camera_index = self.get_selected_camera_index()
                if hasattr(camera, "start_camera"):
                    camera.start_camera(camera_index)

                self.expand_window._camera_widget = camera
            except Exception:
                tk.Label(
                    large_host,
                    text="Không thể mở camera lớn.",
                    font=("Segoe UI", 12, "bold"),
                    fg=Colors.TEXT,
                    bg="#080b0e",
                ).place(relx=0.5, rely=0.5, anchor="center")

        self.expand_window.protocol("WM_DELETE_WINDOW", self._close_large_view)

    def _close_large_view(self):
        if self.expand_window is None:
            return

        try:
            camera = getattr(self.expand_window, "_camera_widget", None)
            if camera is not None and hasattr(camera, "stop_camera"):
                camera.stop_camera()
            self.expand_window.destroy()
        except tk.TclError:
            pass

        self.expand_window = None
