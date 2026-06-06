import cv2
import os
from datetime import datetime


class ImageLogger:

    def __init__(self):

        os.makedirs(
            "images/OK",
            exist_ok=True
        )

        os.makedirs(
            "images/NG",
            exist_ok=True
        )

    def save(
        self,
        image,
        result
    ):

        if image is None:
            return ""

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        path = f"images/{result}/{timestamp}.jpg"

        cv2.imwrite(
            path,
            image
        )

        return path