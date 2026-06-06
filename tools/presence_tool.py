import cv2
import numpy as np


class PresenceTool:

    def __init__(
        self,
        threshold=30
    ):

        self.threshold = threshold

    def inspect(self, image):

        if image is None:

            return {
                "result": "NG",
                "score": 0
            }

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        std = np.std(gray)

        result = (
            "OK"
            if std > self.threshold
            else "NG"
        )

        return {
            "result": result,
            "score": float(std)
        }