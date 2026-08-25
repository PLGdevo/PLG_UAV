import tkinter as tk
from tkinter import messagebox

from .Styles import Colors, setup_styles
from .Header import Header
from .Flight_HUD import FlightHUD
from .Map_Container import MapContainer
from .Waypoint_Panel import WaypointPanel
from .Command_Panel import CommandPanel
from .Telemetry_Panel import TelemetryPanel
from .Video_Panel import VideoPanel
from .Log_Panel import LogPanel


class MainWindow:
    """
    RIGEL UI layer.

    Nguyên tắc:
        UI = hiển thị + tương tác người dùng.

    UI KHÔNG chứa:
        - Map engine
        - Map provider
        - GPS conversion
        - MAVLink
        - Telemetry receiver
        - Flight controller
        - Camera processing
        - AI processing
        - Module hardware

    Các thành phần bên ngoài sẽ kết nối qua callback / mount.
    """

    def __init__(self, root):
        self.root = root

        self.root.title(
            "RIGEL Ground Control Station v1.0 - "
            "[Trạm Điều Khiển Bay Mặt Đất]"
        )
        self.root.geometry("1280x800")
        self.root.minsize(1100, 700)
        self.root.configure(bg=Colors.BG)

        setup_styles(root)

        # UI state only.
        self.flight_mode = "DISARMED"
        self.is_armed = False

        # Demo display data only.
        self.demo_alt = 0.0
        self.demo_speed = 0.0
        self.demo_heading = 120.0
        self.demo_pitch = 0.0
        self.demo_roll = 0.0

        self._build_header()
        self._build_layout()
        self._bind_events()

        self.log("RIGEL GCS UI initialized.")
        self.log("MAP INTERFACE: waiting for external module.")
        self.log("VIDEO MODULE: waiting for external module.")
        self.log("TELEMETRY: waiting for external source.")

        # Chỉ để test UI.
        self._demo_loop()

    # ============================================================
    # BUILD UI
    # ============================================================

    def _build_header(self):
        self.header = Header(self.root)

    def _build_layout(self):
        root_container = tk.Frame(self.root, bg=Colors.BG)
        root_container.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        # --------------------------------------------------------
        # LEFT
        # --------------------------------------------------------
        left = tk.Frame(
            root_container,
            bg=Colors.CARD,
            width=320,
            bd=1,
            relief="solid",
        )
        left.pack(side="left", fill="y", padx=4)
        left.pack_propagate(False)

        self.hud = FlightHUD(left)
        self.hud.frame.pack(fill="x")

        # Camera cố định ngay dưới trạng thái drone (Flight HUD).
        self.video_panel = VideoPanel(
            left,
            on_camera_change=self._on_camera_change,
        )

        self.telemetry_panel = TelemetryPanel(left)

        # --------------------------------------------------------
        # CENTER
        # --------------------------------------------------------
        center = tk.Frame(
            root_container,
            bg=Colors.CARD,
            bd=1,
            relief="solid",
        )
        center.pack(side="left", fill="both", expand=True, padx=4)

        self.map_container = MapContainer(center)
        self.map_container.frame.pack(fill="both", expand=True)

        # --------------------------------------------------------
        # RIGHT
        # --------------------------------------------------------
        right = tk.Frame(
            root_container,
            bg=Colors.CARD,
            width=320,
            bd=1,
            relief="solid",
        )
        right.pack(side="right", fill="y", padx=4)
        right.pack_propagate(False)

        self.waypoint_panel = WaypointPanel(
            right,
            on_delete=self._on_delete_waypoint,
            on_clear=self._on_clear_waypoints,
            on_select=self._on_select_waypoint,
        )
        self.waypoint_panel.frame.pack(fill="x")

        self.command_panel = CommandPanel(
            right,
            on_command=self._on_command,
        )
        self.command_panel.frame.pack(fill="x")

        self.log_panel = LogPanel(right)
        self.log_panel.frame.pack(fill="both", expand=True)

    def _bind_events(self):
        self.root.bind(
            "<Delete>",
            lambda _event: self._on_delete_waypoint()
        )

    # ============================================================
    # EXTERNAL MODULE MOUNTING
    # ============================================================

    def mount_map_interface(self, widget):
        """
        MAP_INTERFACE gọi hàm này để nhúng bản đồ vào UI.
        """
        self.map_container.mount(widget)
        self.map_container.set_provider_status(
            "MAP INTERFACE: CONNECTED"
        )
        self.log("MAP INTERFACE mounted.")

    def mount_video_module(self, widget):
        """
        Camera/Video module gọi hàm này để nhúng video.
        """
        self.video_panel.mount(widget)
        self.video_panel.set_status("VIDEO: CONNECTED")
        self.log("VIDEO MODULE mounted.")

    # ============================================================
    # UI CALLBACKS
    # ============================================================

    def _on_camera_change(self, camera_index):
        self.log(f"CAMERA UI: chọn Camera {camera_index}")

    def _on_command(self, command):
        """
        Hiện tại chỉ mô phỏng UI state.
        Sau này thay callback này bằng Controller.
        """
        if command == "ARM":
            if not self.is_armed:
                self.is_armed = True
                self.flight_mode = "ARMED"
                self.command_panel.set_armed(True)
                self.header.set_mode(self.flight_mode)
                self.log("COMMAND UI: ARM")
            else:
                if self.demo_alt > 1:
                    messagebox.showwarning(
                        "Safety",
                        "Không thể DISARM khi UAV đang ở trên không.",
                    )
                    return

                self.is_armed = False
                self.flight_mode = "DISARMED"
                self.command_panel.set_armed(False)
                self.header.set_mode(self.flight_mode)
                self.log("COMMAND UI: DISARM")

        elif command == "TAKEOFF":
            if not self.is_armed:
                messagebox.showwarning(
                    "Safety",
                    "UAV chưa ARM.",
                )
                return

            self.flight_mode = "TAKEOFF"
            self.header.set_mode(self.flight_mode)
            self.log("COMMAND UI: TAKEOFF")

        elif command == "RTL":
            if not self.is_armed:
                return

            self.flight_mode = "RTL"
            self.header.set_mode(self.flight_mode)
            self.log("COMMAND UI: RTL")

        elif command == "LAND":
            if not self.is_armed:
                return

            self.flight_mode = "LAND"
            self.header.set_mode(self.flight_mode)
            self.log("COMMAND UI: LAND")

        elif command == "PAUSE":
            if not self.is_armed:
                return

            self.flight_mode = "PAUSE"
            self.header.set_mode(self.flight_mode)
            self.log("COMMAND UI: PAUSE")

    def _on_delete_waypoint(self):
        self.log(
            "UI: yêu cầu xóa waypoint -> chờ MAP_INTERFACE."
        )

    def _on_clear_waypoints(self):
        self.log(
            "UI: yêu cầu xóa toàn bộ waypoint -> chờ MAP_INTERFACE."
        )

    def _on_select_waypoint(self, index):
        self.log(
            f"UI: chọn waypoint index={index}."
        )

    # ============================================================
    # DATA INPUT API
    # ============================================================

    def update_flight_state(
        self,
        altitude=None,
        speed=None,
        heading=None,
        pitch=None,
        roll=None,
    ):
        """
        API để Controller/Telemetry cập nhật dữ liệu hiển thị.
        """
        if altitude is not None:
            self.demo_alt = altitude
        if speed is not None:
            self.demo_speed = speed
        if heading is not None:
            self.demo_heading = heading
        if pitch is not None:
            self.demo_pitch = pitch
        if roll is not None:
            self.demo_roll = roll

        self.hud.update(
            self.demo_alt,
            self.demo_speed,
            self.demo_heading,
            self.demo_pitch,
            self.demo_roll,
        )

    def update_system_state(
        self,
        battery_pct=None,
        voltage=None,
        satellites=None,
        fix_type=None,
        signal_pct=None,
        signal_dbm=None,
    ):
        """
        API để Telemetry/Controller cập nhật panel hệ thống.
        """
        self.telemetry_panel.update(
            battery_pct=battery_pct,
            voltage=voltage,
            satellites=satellites,
            fix_type=fix_type,
            signal_pct=signal_pct,
            signal_dbm=signal_dbm,
        )

    def update_waypoints(self, waypoints, selected_index=None):
        """
        API để MAP_INTERFACE cập nhật danh sách waypoint cho UI.
        """
        self.waypoint_panel.set_waypoints(
            waypoints,
            selected_index,
        )

    def set_telemetry_status(self, online):
        self.header.set_telemetry(online)

    def set_gcs_status(self, status):
        self.header.set_gcs_status(status)

    # ============================================================
    # LOG
    # ============================================================

    def log(self, message):
        if hasattr(self, "log_panel"):
            self.log_panel.write(message)

    # ============================================================
    # DEMO UI ONLY
    # ============================================================

    def _demo_loop(self):
        """
        Demo để chạy UI độc lập.

        Có thể xóa hàm này khi Controller + Telemetry thật
        được kết nối.
        """
        if self.is_armed and self.flight_mode == "TAKEOFF":
            self.demo_alt = min(150.0, self.demo_alt + 1.5)
            self.demo_speed = 8.0

            if self.demo_alt >= 150:
                self.flight_mode = "AUTO_MISSION"
                self.header.set_mode(self.flight_mode)
                self.log("DEMO: TAKEOFF COMPLETE")

        elif self.is_armed and self.flight_mode == "AUTO_MISSION":
            self.demo_speed = 40.0
            self.demo_heading = (self.demo_heading + 0.5) % 360
            self.demo_pitch = -2.0
            self.demo_roll = 3.0

        elif self.is_armed and self.flight_mode == "RTL":
            self.demo_speed = 30.0
            self.demo_heading = (self.demo_heading + 0.8) % 360
            self.demo_pitch = -1.0
            self.demo_roll = 2.0

        elif self.is_armed and self.flight_mode == "LAND":
            self.demo_speed = 3.0
            self.demo_alt = max(0.0, self.demo_alt - 0.8)

            if self.demo_alt <= 0:
                self.demo_alt = 0
                self.demo_speed = 0
                self.is_armed = False
                self.flight_mode = "DISARMED"
                self.command_panel.set_armed(False)
                self.header.set_mode(self.flight_mode)
                self.log("DEMO: LAND COMPLETE")

        elif self.is_armed and self.flight_mode == "PAUSE":
            self.demo_speed = 0
            self.demo_pitch = 0
            self.demo_roll = 0

        self.update_flight_state(
            altitude=self.demo_alt,
            speed=self.demo_speed,
            heading=self.demo_heading,
            pitch=self.demo_pitch,
            roll=self.demo_roll,
        )

        # self.root.after(50, self._demo_loop)
