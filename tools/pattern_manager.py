import os
import cv2


class PatternManager:

    def __init__(self):

        self.master_dir = "masters"

        os.makedirs(
            self.master_dir,
            exist_ok=True
        )

    def save_master(
        self,
        roi_index,
        image
    ):

        path = os.path.join(
            self.master_dir,
            f"roi_{roi_index}.png"
        )

        cv2.imwrite(
            path,
            image
        )

    def load_master(
        self,
        roi_index
    ):

        path = os.path.join(
            self.master_dir,
            f"roi_{roi_index}.png"
        )

        if not os.path.exists(path):
            return None

        return cv2.imread(path)