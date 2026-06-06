import cv2

class ReferenceTool:

    def find_offset(
        self,
        image,
        master,
        ref_x,
        ref_y
    ):

        if image is None or master is None:
            return False,0,0,0

        gray_img = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray_master = cv2.cvtColor(
            master,
            cv2.COLOR_BGR2GRAY
        )

        result = cv2.matchTemplate(
            gray_img,
            gray_master,
            cv2.TM_CCOEFF_NORMED
        )

        _, score, _, max_loc = cv2.minMaxLoc(result)

        dx = max_loc[0] - ref_x
        dy = max_loc[1] - ref_y

        print(
            f"REF_X={ref_x} "
            f"REF_Y={ref_y}"
        )

        print(
            f"MATCH_X={max_loc[0]} "
            f"MATCH_Y={max_loc[1]}"
        )

        return True, dx, dy, score * 100