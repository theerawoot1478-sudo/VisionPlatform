import cv2

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QImage,
    QPainter,
    QPen
)
from PyQt5.QtCore import (
    Qt,
    QRect,
    QPoint
)


class CameraWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setMinimumSize(800, 600)

        self.frame = None

        self.roi_list = []

        self.dragging = False

        self.start_point = QPoint()
        self.end_point = QPoint()
        self.roi_results = {}
        self.offset_dx = 0
        self.offset_dy = 0

    def update_image(self, frame):

        self.frame = frame.copy()

        self.update()

    def clear_roi(self):

        self.roi_list.clear()

        self.update()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.start_point = event.pos()
            self.end_point = event.pos()

    def mouseMoveEvent(self, event):

        if self.dragging:

            self.end_point = event.pos()

            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            self.end_point = event.pos()

            rect = QRect(
                self.start_point,
                self.end_point
            ).normalized()

            if rect.width() > 10 and rect.height() > 10:

                self.roi_list.append(rect)

                print(
                    f"ROI {len(self.roi_list)} : "
                    f"{rect.x()}, "
                    f"{rect.y()}, "
                    f"{rect.width()}, "
                    f"{rect.height()}"
                )

            self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        if self.frame is not None:

            rgb = cv2.cvtColor(
                self.frame,
                cv2.COLOR_BGR2RGB
            )

            h, w, ch = rgb.shape

            image = QImage(
                rgb.data,
                w,
                h,
                ch * w,
                QImage.Format_RGB888
            )

            painter.drawImage(
                self.rect(),
                image
            )

        pen = QPen(Qt.green)

        pen.setWidth(2)

        painter.setPen(pen)
        #print("PAINT",self.roi_results)

        for index, roi in enumerate(
            self.roi_list
        ):

            if index in self.roi_results:

                result = self.roi_results[index]

                if result["result"] == "OK":

                    painter.setPen(
                        QPen(
                            Qt.green,
                            2
                        )
                    )

                else:

                    painter.setPen(
                        QPen(
                            Qt.red,
                            2
                        )
                    )

            else:

                painter.setPen(
                    QPen(
                        Qt.green,
                        2
                    )
                )

            draw_roi = QRect(
                roi.x() + self.offset_dx,
                roi.y() + self.offset_dy,
                roi.width(),
                roi.height()
            )

            painter.drawRect(draw_roi)

            if index in self.roi_results:

                text = (
                    f"ROI{index+1}\n"
                    f"{result['result']}\n"
                    f"{result['score']:.1f}"
                )

                painter.drawText(

                    roi.x(),

                    roi.y() - 5,

                    text

                )

        if self.dragging:

            temp_rect = QRect(
                self.start_point,
                self.end_point
            ).normalized()

            painter.drawRect(temp_rect)
    
    def get_roi_image(
        self,
        frame,
        roi_index=0,
        dx=0,
        dy=0
    ):

        if frame is None:
            return None

        if len(self.roi_list) == 0:
            return None

        if roi_index >= len(self.roi_list):
            return None

        roi = self.roi_list[roi_index]

        frame_h, frame_w = frame.shape[:2]

        widget_w = self.width()
        widget_h = self.height()

        scale_x = frame_w / widget_w
        scale_y = frame_h / widget_h

        x = int(roi.x() * scale_x) + dx
        y = int(roi.y() * scale_y) + dy

        w = int(roi.width() * scale_x)
        h = int(roi.height() * scale_y)

        x = max(0, x)
        y = max(0, y)

        if x + w > frame_w:
            w = frame_w - x

        if y + h > frame_h:
            h = frame_h - y
        
        if w <= 0 or h <= 0:
            return None

        print(
            f"ROI IMAGE : "
            f"X={x} Y={y} W={w} H={h}"
        )

        crop = frame[
            y:y+h,
            x:x+w
        ]

        return crop
    
    def set_roi_result(
        self,
        roi_index,
        result,
        score
    ):

        print(
            "SET ROI RESULT:",
            roi_index,
            result,
            score
        )

        self.roi_results[roi_index] = {
            "result": result,
            "score": score
        }

        self.update()