import cv2


class CameraManager:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception(
                f"Cannot open camera {camera_index}"
            )

    def read(self):

        return self.cap.read()

    def release(self):

        if self.cap:
            self.cap.release()