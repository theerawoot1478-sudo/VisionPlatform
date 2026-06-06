import cv2
import numpy as np


class BrightnessTool:

    def __init__(
        self,
        min_value=50,
        max_value=200
    ):

        self.min_value = min_value
        self.max_value = max_value

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

        mean_value = np.mean(
            gray
        )

        result = (
            "OK"
            if self.min_value
            <= mean_value
            <= self.max_value
            else "NG"
        )

        return {
            "result": result,
            "score": float(mean_value)
        }