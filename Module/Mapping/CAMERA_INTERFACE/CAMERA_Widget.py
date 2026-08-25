import tkinter as tk
import cv2

from PIL import Image, ImageTk

from .CAMERA_Device import CameraDevice


class CameraWidget(tk.Frame):
    """
    Camera preview nhỏ cho RIGEL GCS.

    Chức năng:
        - Hiển thị hình ảnh realtime từ camera.
        - Không mirror hình ảnh.
        - Có nút RELOAD để kết nối lại camera.
        - Ghi nhớ camera/device đang được chọn.
    """

    def __init__(
        self,
        parent,
        width=256,
        height=128,
        **kwargs
    ):

        super().__init__(
            parent,
            bg="black",
            highlightthickness=1,
            highlightbackground="#555555",
            **kwargs
        )

        self.preview_width = width
        self.preview_height = height

        # =====================================================
        # CAMERA STATE
        # =====================================================

        self.camera = None
        self.running = False
        self.photo = None

        # Camera hiện tại
        self.device_index = 0

        # =====================================================
        # VIDEO
        # =====================================================

        self.video_label = tk.Label(
            self,
            bg="black",
            bd=0,
            highlightthickness=0
        )

        self.video_label.pack(
            fill=tk.BOTH,
            expand=True
        )

        # =====================================================
        # CAMERA CONTROLS
        # =====================================================

        self.control_frame = tk.Frame(self,bg="#111111",height=30)

        self.control_frame.pack(
            fill=tk.X,
            side=tk.BOTTOM
        )

        self.control_frame.pack_propagate(False)

        # -----------------------------------------------------
        # RELOAD BUTTON
        # -----------------------------------------------------

        self.reload_button = tk.Button(
            self.control_frame,
            text="↻ RELOAD",
            command=self.reload_camera,
            bg="#222222",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )

        self.reload_button.pack(
            side=tk.RIGHT,
            padx=4,
            pady=3
        )

    # =========================================================
    # START CAMERA
    # =========================================================

    def start_camera(self, device_index=0):

        # Lưu camera đang sử dụng
        self.device_index = device_index

        # Đóng camera cũ trước
        self.stop_camera()

        # Tạo camera mới
        self.camera = CameraDevice(
            device_index=device_index,
            width=1280,
            height=720
        )

        # Mở camera
        if not self.camera.open():

            self.camera = None
            self.running = False

            self.video_label.config(
                image="",
                text="NO CAMERA",
                fg="white",
                bg="black",
                font=("Segoe UI", 12)
            )

            return False

        # Camera đã mở thành công
        self.running = True

        self.video_label.config(
            text=""
        )

        # Bắt đầu đọc frame
        self.update_frame()

        return True

    # =========================================================
    # RELOAD CAMERA
    # =========================================================

    def reload_camera(self):
        device_index = self.device_index

        # Disable nút trong lúc reload
        self.reload_button.config(
            state=tk.DISABLED,
            text="↻ RELOADING..."
        )

        self.update_idletasks()

        # Đóng và mở lại camera
        success = self.start_camera(
            device_index=device_index
        )

        # Khôi phục nút
        self.reload_button.config(
            state=tk.NORMAL,
            text="↻ RELOAD"
        )

        return success

    # =========================================================
    # UPDATE FRAME
    # =========================================================

    def update_frame(self):

        if not self.running:
            return

        if self.camera is None:
            return

        # Đọc frame
        frame = self.camera.read()

        # Không nhận được frame
        if frame is None:

            self.stop_camera()

            self.video_label.config(
                image="",
                text="NO SIGNAL",
                fg="white",
                bg="black",
                font=("Segoe UI", 12)
            )

            return

        # -----------------------------------------------------
        # KHÔNG MIRROR
        # -----------------------------------------------------

        # Nếu muốn mirror camera:
        #
        # frame = cv2.flip(frame, 1)

        # -----------------------------------------------------
        # BGR -> RGB
        # -----------------------------------------------------

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # -----------------------------------------------------
        # KÍCH THƯỚC WIDGET THỰC TẾ
        # -----------------------------------------------------

        widget_width = self.video_label.winfo_width()
        widget_height = self.video_label.winfo_height()

        if widget_width > 10 and widget_height > 10:

            frame = self.resize_keep_ratio(
                frame,
                widget_width,
                widget_height
            )

        # -----------------------------------------------------
        # PIL IMAGE
        # -----------------------------------------------------

        image = Image.fromarray(frame)

        # -----------------------------------------------------
        # TKINTER IMAGE
        # -----------------------------------------------------

        self.photo = ImageTk.PhotoImage(
            image=image
        )

        self.video_label.config(
            image=self.photo,
            text=""
        )

        # -----------------------------------------------------
        # ~30 FPS
        # -----------------------------------------------------

        self.after(
            30,
            self.update_frame
        )

    # =========================================================
    # RESIZE KEEP RATIO
    # =========================================================

    @staticmethod
    def resize_keep_ratio(
        frame,
        target_width,
        target_height
    ):

        height, width = frame.shape[:2]

        if width <= 0 or height <= 0:
            return frame

        scale = min(
            target_width / width,
            target_height / height
        )

        new_width = max(
            1,
            int(width * scale)
        )

        new_height = max(
            1,
            int(height * scale)
        )

        return cv2.resize(
            frame,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    # =========================================================
    # STOP CAMERA
    # =========================================================

    def stop_camera(self):

        self.running = False

        if self.camera is not None:

            try:
                self.camera.release()
            except Exception:
                pass

            self.camera = None

        self.photo = None

        self.video_label.config(
            image="",
            text=""
        )

    # =========================================================
    # DESTROY
    # =========================================================

    def destroy(self):

        self.stop_camera()

        super().destroy()