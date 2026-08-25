import cv2


class CameraDevice:
    """
    Quản lý camera vật lý.

    Hỗ trợ:
        - Camera laptop
        - USB Webcam
        - USB Camera
        - Các thiết bị camera tương thích OpenCV
    """

    def __init__(self, device_index=0, width=1280, height=720):
        self.device_index = device_index
        self.width = width
        self.height = height

        self.cap = None
        self.is_open = False

    # =========================================================
    # OPEN CAMERA
    # =========================================================

    def open(self):
        """
        Mở camera.
        """

        if self.is_open:
            return True

        self.cap = cv2.VideoCapture(
            self.device_index,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.is_open = False
            return False

        # Cấu hình độ phân giải
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.is_open = True

        return True

    # =========================================================
    # READ FRAME
    # =========================================================

    def read(self):
        """
        Đọc một frame từ camera.

        Returns:
            frame nếu thành công
            None nếu thất bại
        """

        if not self.is_open or self.cap is None:
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    # =========================================================
    # RELEASE
    # =========================================================

    def release(self):

        if self.cap is not None:
            self.cap.release()

        self.cap = None
        self.is_open = False

    # =========================================================
    # CAMERA INFORMATION
    # =========================================================

    def get_resolution(self):

        if not self.is_open or self.cap is None:
            return None

        width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        return width, height

    # =========================================================
    # CHECK CAMERA
    # =========================================================

    @staticmethod
    def is_available(index):

        cap = cv2.VideoCapture(
            index,
            cv2.CAP_DSHOW
        )

        available = cap.isOpened()

        cap.release()

        return available

    # =========================================================
    # SCAN CAMERAS
    # =========================================================

    @staticmethod
    def scan(max_devices=10):

        devices = []

        for index in range(max_devices):

            if CameraDevice.is_available(index):
                devices.append(index)

        return devices