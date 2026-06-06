import cv2
import numpy as np

class PatternTool:

    def __init__(self,threshold=80):
        self.threshold = threshold
        self.master = None

    def set_master(self, image):
        if image is None:
            return
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )
        self.master = gray

    def inspect(self, image):
        if image is None:
            return {
                "result": "NG",
                "score": 0
            }
        if image.shape[0] == 0 or image.shape[1] == 0:
            return {
                "result":"NG",
                "score":0
            }
        if self.master is None:
            return {
                "result": "NO_MASTER",
                "score": 0
            }
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )
        gray = cv2.resize(
            gray,
            (
                self.master.shape[1],
                self.master.shape[0]
            )
        )
        score = cv2.matchTemplate(
            gray,
            self.master,
            cv2.TM_CCOEFF_NORMED
        )[0][0]
        score = score * 100
        result = (
            "OK"
            if score >= self.threshold
            else "NG"
        )
        return {
            "result": result,
            "score": float(score)
        }
    
    def inspect_with_master(
        self,
        image,
        master
    ):
        if master is None:
            return {
                "result": "NG",
                "score": 0
            }

        if image.shape != master.shape:

            master = cv2.resize(
                master,
                (
                    image.shape[1],
                    image.shape[0]
                )
            )

        result = cv2.matchTemplate(
            image,
            master,
            cv2.TM_CCOEFF_NORMED
        )

        score = float(
            result.max()
        ) * 100

        return {

            "result":
            "OK"
            if score >= self.threshold
            else "NG",

            "score": score

        }