import csv
import matplotlib.pyplot as plt
import time
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QInputDialog
)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from tools.brightness_tool import BrightnessTool
from tools.presence_tool import PresenceTool
from tools.pattern_tool import PatternTool
from core.recipe_manager import RecipeManager
from core.statistics import Statistics
from core.database import Database
from core.image_logger import ImageLogger
from core.tool_manager import ToolManager
from tools.ocr_tool import OCRTool
from tools.pattern_manager import PatternManager
from core.plc_manager import PLCManager
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from core.user_manager import UserManager
from core.audit_logger import AuditLogger
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QPixmap
from tools.reference_tool import ReferenceTool

from PyQt5.QtCore import QTimer
from core.camera_manager import CameraManager
from ui.camera_widget import CameraWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision Platform Enterprise")
        self.resize(1400, 900)
        self.camera = CameraManager(0)
        self.brightness_tool = BrightnessTool(min_value=50,max_value=200)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)
        self.camera_widget = CameraWidget()
        main_layout.addWidget(self.camera_widget,stretch=4)
        right_container = QWidget()
        right_panel = QVBoxLayout(right_container)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(right_container)
        self.machine_label = QLabel("STATE : READY")
        right_panel.addWidget(self.machine_label)
        self.cycle_time_label = QLabel("CYCLE : 0 ms")
        right_panel.addWidget(self.cycle_time_label)
        self.alarm_label = QLabel(
            "PATTERN:0\n"
            "PRESENCE:0\n"
            "OCR:0\n"
            "BRIGHT:0\n"
            "TIMEOUT:0"
        )
        self.oee_label = QLabel(
            "A:0%\n"
            "P:0%\n"
            "Q:0%\n"
            "OEE:0%"
        )
        right_panel.addWidget(
            self.oee_label
        )
        right_panel.addWidget(self.alarm_label)
        self.roi_label = QLabel("ROI : 0")
        right_panel.addWidget(self.roi_label)
        self.presence_tool = PresenceTool(threshold=20)
        self.pattern_tool = PatternTool(threshold=80)
        self.auto_mode = False
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_inspect)
        self.recipe_manager = RecipeManager()
        self.statistics = Statistics()
        self.database = Database()
        self.image_logger = ImageLogger()
        self.tool_manager = ToolManager()
        self.ocr_tool = OCRTool()
        self.pattern_manager = PatternManager()
        self.plc = PLCManager()
        self.user_manager = UserManager()
        self.audit_logger = AuditLogger()
        self.reference_tool = ReferenceTool()
        
        self.current_role = "operator"
        self.current_user = {"username": "GUEST","role": "operator"}
        self.machine_state = "READY"
        self.set_machine_state("READY")
        self.last_cycle_time = 0
        self.cycle_start_time = 0
        self.timeout_limit = 3000
        self.alarm_counter = {
            "NG_PATTERN":0,
            "NG_PRESENCE":0,
            "NG_OCR":0,
            "NG_BRIGHTNESS":0,
            "TIMEOUT":0
        }
        self.total_cycle = 0
        self.total_runtime = 0
        self.good_count = 0
        self.ideal_cycle_time = 500
        self.reference_enabled = False
        self.reference_roi_index = 0
        self.reference_threshold = 70
        self.reference_x = 0
        self.reference_y = 0

        self.login_btn = QPushButton("Login")
        self.logout_btn = QPushButton("Logout")
        self.add_user_btn = QPushButton("Add User")
        self.delete_user_btn = QPushButton("Delete User")
        self.change_password_btn = QPushButton("Change Password")
        self.audit_btn = QPushButton("Audit Log")
        self.history_btn = QPushButton("History")
        self.trend_btn = QPushButton("Trend Graph")
        self.export_btn = QPushButton("Export CSV")
        self.pdf_btn = QPushButton("Export PDF")

        self.user_label = QLabel("USER : GUEST")
        self.recipe_label = QLabel("Recipe : NONE")
        self.recipe_name = QLineEdit()
        self.exposure_edit = QLineEdit()
        self.gain_edit = QLineEdit()
        self.gain_edit.setText("1.0")
        self.exposure_edit.setText("100")
        self.recipe_name.setText("Recipe_01")
        self.recipe_list = QComboBox()
        self.history_filter = QComboBox()
        self.history_filter.addItems(["ALL","OK","NG"])
        self.history_filter.currentTextChanged.connect(self.filter_history)
        self.recipe_list.currentTextChanged.connect(self.recipe_selected)
        self.result_label = QLabel("Result : READY")
        self.stats_label = QLabel("TOTAL : 0\n""OK : 0\n""NG : 0\n""YIELD : 0%")
        self.log_box = QTextEdit()
        self.history_table = QTableWidget()
        self.image_preview = QLabel()
        self.image_preview.setMinimumHeight(250)
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(["ID","DATETIME","RECIPE","RESULT","REASON","SCORE","IMAGE"])
        self.history_table.setMinimumHeight(250)
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(200)
        
        self.role_label = QLabel(f"ROLE : {self.current_role}")
        right_panel.addWidget(self.role_label)
        right_panel.addWidget(self.user_label)
        right_panel.addWidget(self.recipe_label)
        right_panel.addWidget(self.recipe_name)
        right_panel.addWidget(QLabel("Exposure"))
        right_panel.addWidget(self.exposure_edit)
        right_panel.addWidget(QLabel("Gain"))
        right_panel.addWidget(self.gain_edit)
        right_panel.addWidget(self.recipe_list)
        right_panel.addWidget(self.history_filter)
        right_panel.addWidget(self.result_label)
        right_panel.addWidget(self.stats_label)
        right_panel.addWidget(self.log_box)
        right_panel.addWidget(self.history_table)
        right_panel.addWidget(self.image_preview)
        
        self.search_recipe_btn = QPushButton("Search Recipe")
        self.clear_btn = QPushButton("Clear ROI")
        self.test_btn = QPushButton("Test ROI")
        self.inspect_btn = QPushButton("Inspect")
        self.presence_btn = QPushButton("Presence")
        self.master_btn = QPushButton("Set Master")
        self.reference_btn = QPushButton("Set Reference")
        self.pattern_btn = QPushButton("Pattern")
        self.save_recipe_btn = QPushButton("Save Recipe")
        self.load_recipe_btn = QPushButton("Load Recipe")
        self.inspect_all_btn = QPushButton("Inspect All")
        self.assign_btn = QPushButton("Assign Tools")
        self.show_tools_btn = QPushButton("Show Tools")
        self.ocr_btn = QPushButton("OCR")
        self.auto_btn = QPushButton("Start Auto")
        self.trigger_btn = QPushButton("PLC Trigger")
        self.plc_test_btn = QPushButton("PLC Test")

        self.login_btn.clicked.connect(self.login)
        right_panel.addWidget(self.login_btn)
        self.logout_btn.clicked.connect(self.logout)
        right_panel.addWidget(self.logout_btn)
        self.add_user_btn.clicked.connect(self.add_user)
        right_panel.addWidget(self.add_user_btn)
        self.delete_user_btn.clicked.connect(self.delete_user)
        right_panel.addWidget(self.delete_user_btn)
        self.change_password_btn.clicked.connect(self.change_password)
        right_panel.addWidget(self.change_password_btn)
        self.audit_btn.clicked.connect(self.show_audit_log)
        right_panel.addWidget(self.audit_btn)
        self.history_btn.clicked.connect(self.show_history)
        right_panel.addWidget(self.history_btn)
        self.trend_btn.clicked.connect(self.show_trend)
        right_panel.addWidget(self.trend_btn)
        
        self.export_btn.clicked.connect(self.export_csv)
        right_panel.addWidget(self.export_btn)
        
        self.pdf_btn.clicked.connect(self.export_pdf)
        right_panel.addWidget(self.pdf_btn)
        self.search_recipe_btn.clicked.connect(self.search_recipe_history)
        right_panel.addWidget(self.search_recipe_btn)

        self.clear_btn.clicked.connect(self.clear_roi)
        right_panel.addWidget(self.clear_btn)
        self.plc_test_btn.clicked.connect(self.test_plc)
        right_panel.addWidget(self.plc_test_btn)
        self.trigger_btn.clicked.connect(self.fake_trigger)
        right_panel.addWidget(self.trigger_btn)
        self.auto_btn.clicked.connect(self.toggle_auto)
        right_panel.addWidget(self.auto_btn)
        self.ocr_btn.clicked.connect(self.ocr_check)
        right_panel.addWidget(self.ocr_btn)
        self.show_tools_btn.clicked.connect(self.show_tools)
        right_panel.addWidget(self.show_tools_btn)
        self.assign_btn.clicked.connect(self.assign_tools)
        right_panel.addWidget(self.assign_btn)
        self.inspect_all_btn.clicked.connect(self.inspect_all)
        right_panel.addWidget(self.inspect_all_btn)
        self.load_recipe_btn.clicked.connect(self.load_recipe)
        right_panel.addWidget(self.load_recipe_btn)
        self.save_recipe_btn.clicked.connect(self.save_recipe)
        right_panel.addWidget(self.save_recipe_btn)
        self.pattern_btn.clicked.connect(self.pattern_check)
        right_panel.addWidget(self.pattern_btn)
        self.master_btn.clicked.connect(self.set_master)
        right_panel.addWidget(self.master_btn)
        self.reference_btn.clicked.connect(self.set_reference)
        right_panel.addWidget(self.reference_btn)
        self.presence_btn.clicked.connect(self.presence_check)
        right_panel.addWidget(self.presence_btn)
        self.inspect_btn.clicked.connect(self.inspect)
        right_panel.addWidget(self.inspect_btn)
        self.test_btn.clicked.connect(self.test_roi)
        right_panel.addWidget(self.test_btn)
        #right_panel.addStretch()
        main_layout.addWidget(scroll,stretch=1)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)
        self.refresh_recipe_list()
        self.show_history()
        rows = self.database.get_all()
        for row in rows:self.statistics.add_result(row[3])
        self.update_statistics()
        self.history_table.cellClicked.connect(self.history_row_clicked)
        self.update_permission()
        

    def update_camera(self):
        ret, frame = self.camera.read()
        if not ret:
            return
        self.current_frame = frame
        self.camera_widget.update_image(frame)
        self.roi_label.setText(f"ROI : {len(self.camera_widget.roi_list)}")

    def clear_roi(self):
        self.camera_widget.clear_roi()
        self.tool_manager.clear()

    def closeEvent(self, event):
        self.camera.release()
        event.accept()
    
    def test_roi(self):
        if not hasattr(self,"current_frame"):
            return
        crop = self.camera_widget.get_roi_image(self.current_frame,0)
        if crop is None:
            print("No ROI")
            return
        import cv2
        cv2.imshow("ROI",crop)
        cv2.waitKey(1)
    
    def inspect(self):
        if not hasattr(self,"current_frame"):
            return
        crop = self.camera_widget.get_roi_image(self.current_frame,0)
        if crop is None:
            print("No ROI")
            return
        result = self.brightness_tool.inspect(crop)
        self.result_label.setText(f"Result : {result['result']}")
        self.stats_label.setText(f"Brightness : {result['score']:.2f}")
        print(result)
    
    def presence_check(self):
        if not hasattr(self,"current_frame"):
            return
        crop = self.camera_widget.get_roi_image(self.current_frame,0)
        if crop is None:
            return
        result = self.presence_tool.inspect(crop)
        self.result_label.setText(f"Result : {result['result']}")
        self.stats_label.setText(f"Presence : {result['score']:.2f}")
        print(result)
    
    def set_master(self):
        if not hasattr(self,"current_frame"):
            return
        for index in range(len(self.camera_widget.roi_list)):
            crop = self.camera_widget.get_roi_image(self.current_frame,index)
            if crop is None:
                continue
            self.pattern_manager.save_master(index,crop)
            print(f"MASTER ROI{index+1} SAVED")
        self.result_label.setText("Master Saved")
    
    def pattern_check(self):
        if not hasattr(self,"current_frame"):
            return
        crop = self.camera_widget.get_roi_image(self.current_frame,0)
        if crop is None:
            return
        master = self.pattern_manager.load_master(0)
        result = self.pattern_tool.inspect_with_master(
            crop,
            master
        )
        image_path = self.image_logger.save(
            crop,
            result["result"]
        )
        reason = (
            "OK"
            if result["result"] == "OK"
            else "NG_PATTERN"
        )
        self.database.add_result(
            self.recipe_name.text(),
            result["result"],
            reason,
            result["score"],
            image_path
        )
        self.statistics.add_result(
            result["result"]
        )
        self.update_statistics()
        self.result_label.setText(
            f"Result : {result['result']}"
        )
        self.stats_label.setText(
            f"Pattern : {result['score']:.2f}"
        )
        print(result)

    def save_recipe(self):
        roi_data = []
        for roi in self.camera_widget.roi_list:
            roi_data.append({
                "x": roi.x(),
                "y": roi.y(),
                "w": roi.width(),
                "h": roi.height()
            })
        
        recipe_name = self.recipe_name.text()
        camera_setting = {
            "exposure":
                int(self.exposure_edit.text()),
            "gain":
                float(self.gain_edit.text())
        }
        recipe = {
                "name": recipe_name,
                "camera": camera_setting,
                "rois": roi_data,
                "tools": self.tool_manager.roi_tools,
                "reference": {
                    "x": self.reference_x,
                    "y": self.reference_y
                },

                "thresholds": {
                    "pattern": self.pattern_tool.threshold,
                    "presence": self.presence_tool.threshold,
                    "brightness_min": self.brightness_tool.min_value,
                    "brightness_max": self.brightness_tool.max_value
                }
            }
        self.recipe_manager.save_recipe(recipe_name,recipe)
        self.recipe_label.setText(f"Recipe : {recipe_name}")
        self.refresh_recipe_list()
        print("Recipe Saved")
        self.audit_logger.write(
        self.current_user["username"],"SAVE_RECIPE")

    def load_recipe(self):
        from PyQt5.QtCore import QRect
        recipe_name = self.recipe_name.text()
        recipe = self.recipe_manager.load_recipe(recipe_name)
        ref = recipe.get("reference", {})

        self.reference_x = ref.get("x", 0)
        self.reference_y = ref.get("y", 0)

        print(
            f"REFERENCE LOADED : "
            f"{self.reference_x},"
            f"{self.reference_y}"
        )
        if recipe is None:
            print("Recipe Not Found")
            return
        
        thresholds = recipe.get("thresholds", {})
        self.pattern_tool.threshold = thresholds.get("pattern", 80)
        self.presence_tool.threshold = thresholds.get("presence", 20)
        self.brightness_tool.min_value = thresholds.get("brightness_min", 50)
        self.brightness_tool.max_value = thresholds.get("brightness_max", 200)
    
        camera = recipe.get("camera",{}) 
        self.gain_edit.setText(
            str(
                camera.get("gain",1.0)))
        self.exposure_edit.setText(
            str(
                camera.get("exposure",100)))
        
        self.camera_widget.roi_list.clear()
        for roi in recipe["rois"]:
            self.camera_widget.roi_list.append(
                QRect(
                    roi["x"],
                    roi["y"],
                    roi["w"],
                    roi["h"]
                )
            )
        self.camera_widget.update()
        self.tool_manager.clear()
        tools = recipe.get("tools",{})
        for roi_index, tool_list in tools.items():
            for tool_name in tool_list:
                self.tool_manager.add_tool(int(roi_index),tool_name)
        self.recipe_label.setText(f"Recipe : {recipe_name}")
        print("Recipe Loaded")
        self.audit_logger.write(self.current_user["username"],"LOAD_RECIPE")
        print("TOOLS LOADED:",self.tool_manager.roi_tools)

    def update_statistics(self):
        total = (
            self.statistics.ok_count +
            self.statistics.ng_count
            )
        ng_rate = 0
        if total > 0:
            ng_rate = (
                self.statistics.ng_count
                /
                total
            ) * 100
        self.stats_label.setText(
            f"TOTAL : {total}\n"
            f"OK : {self.statistics.ok_count}\n"
            f"NG : {self.statistics.ng_count}\n"
            f"YIELD : {self.statistics.yield_percent:.2f}%\n"
            f"NG RATE : {ng_rate:.2f}%"
        )
    
    def inspect_all(self):
        #print("INSPECT_ALL START")
        if not hasattr(self,"current_frame"):
            return
        total_result = "OK"
        ng_reason = "OK"
        message = []
        all_scores = []
        dx, dy = self.get_reference_offset()
        print(f"OFFSET = {dx},{dy}")
        self.camera_widget.offset_dx = int(
            dx * self.camera_widget.width()
            / self.current_frame.shape[1]
        )

        self.camera_widget.offset_dy = int(
            dy * self.camera_widget.height()
            / self.current_frame.shape[0]
        )

        self.camera_widget.update()
        if 'dx' in locals() and 'dy' in locals():
            self.log_box.append(f"DX={dx} DY={dy}")
        for index in range(len(self.camera_widget.roi_list)):
            #crop = self.camera_widget.get_roi_image(self.current_frame,index)
            crop = self.camera_widget.get_roi_image(
                self.current_frame,
                index,
                dx,
                dy
            )
            if crop is None:
                print(
                    f"ROI{index} OUT OF RANGE "
                    f"DX={dx} DY={dy}"
                )
                continue

            if crop is None:
                continue
            if crop is None:
                continue
            tools = self.tool_manager.get_tools(index)
            score = 0
            #print("ROI",index,"TOOLS =",tools)
            for tool_name in tools:
                if tool_name == "pattern":
                    master = self.pattern_manager.load_master(index)
                    print("ROI =", index)
                    print("CROP SHAPE =", crop.shape)
                    if master is not None:
                        print("MASTER SHAPE =", master.shape)
                    result = self.pattern_tool.inspect_with_master(crop,master)
                    print("ROI =", index)
                    if crop is None:
                        print("CROP IS NONE")
                    else:
                        print("CROP SHAPE =", crop.shape)
                    if master is None:
                        print("MASTER IS NONE")
                    else:
                        print("MASTER SHAPE =", master.shape)
                    #print("ROI",index,result.get("result"),result.get("score"))
                    self.camera_widget.set_roi_result(
                        index,
                        result.get("result","OK"),
                        result.get("score",100))  
                    score = result.get("score",0)
                    all_scores.append(score)
                    message.append(
                        f"ROI{index+1} "
                        f"{tool_name} "
                        f"{result['result']} "
                        f"({score:.2f})"
                    )
                elif tool_name == "presence":
                    result = self.presence_tool.inspect(crop)
                    #print("ROI",index,result.get("result"),result.get("score"))
                    self.camera_widget.set_roi_result(
                        index,
                        result.get("result","OK"),
                        result.get("score",100))  
                    score = result.get("score",0)
                    all_scores.append(score)
                    message.append(
                        f"ROI{index+1} "
                        f"{tool_name} "
                        f"{result['result']} "
                        f"({score:.2f})"
                    )
                elif tool_name == "brightness":
                    result = self.brightness_tool.inspect(crop)
                    #print("ROI",index,result.get("result"),result.get("score"))
                    self.camera_widget.set_roi_result(
                        index,
                        result.get("result","OK"),
                        result.get("score",100))                     
                    score = result.get("score",0)
                    all_scores.append(score)
                    message.append(
                        f"ROI{index+1} "
                        f"{tool_name} "
                        f"{result['result']} "
                        f"({score:.2f})"
                    )
                elif tool_name == "ocr":
                    result = self.ocr_tool.inspect(crop)
                    self.camera_widget.set_roi_result(
                        index,
                        result.get("result","OK"),
                        result.get("score",100))                   
                    score = result.get("score",0)
                    all_scores.append(score)
                    message.append(
                        f"ROI{index+1} "
                        f"OCR : "
                        f"{result['text']}"
                    )
                else:
                    continue
                #print(f"ROI{index+1}",tool_name,result)
                if result.get("result", "OK") != "OK":
                    if tool_name == "pattern":
                        self.alarm_counter["NG_PATTERN"] += 1
                    elif tool_name == "presence":
                        self.alarm_counter["NG_PRESENCE"] += 1
                    elif tool_name == "ocr":
                        self.alarm_counter["NG_OCR"] += 1
                    elif tool_name == "brightness":
                        self.alarm_counter["NG_BRIGHTNESS"] += 1
                    total_result = "NG"
                    if tool_name == "pattern":
                        ng_reason = "NG_PATTERN"
                    elif tool_name == "presence":
                        ng_reason = "NG_PRESENCE"
                    elif tool_name == "ocr":
                        ng_reason = "NG_OCR"
                    elif tool_name == "brightness":
                        ng_reason = "NG_BRIGHTNESS"
        image_path = self.image_logger.save(self.current_frame,total_result)
        final_score = sum(all_scores) / len(all_scores) if all_scores else 0
        self.database.add_result(
            self.recipe_name.text(),
            total_result,
            ng_reason,
            final_score,
            image_path
        )   
        self.statistics.add_result(total_result)
        self.update_statistics()
        self.show_history()
        if total_result == "OK":
            self.result_label.setText("FINAL : OK")
        else:
            self.result_label.setText(f"FINAL : {ng_reason}")
        cycle_time = int(
            (time.time() - self.cycle_start_time) * 1000
        )
        self.last_cycle_time = cycle_time
        self.total_cycle += 1
        self.total_runtime += (
            cycle_time / 1000
        )
        self.cycle_time_label.setText(
            f"CYCLE : {cycle_time} ms"
        )
        if cycle_time > self.timeout_limit:
            self.alarm_counter["TIMEOUT"] += 1
            self.log_box.append(
                f"TIMEOUT : {cycle_time} ms"
            )
            self.set_machine_state("NG")
        #print("FINAL RESULT =", total_result)
        if total_result == "OK":
            self.good_count += 1
            self.set_machine_state("OK")
            self.plc.write_ok()
        else:
            self.set_machine_state("NG")
            self.plc.write_ng()
        time.sleep(0.3)
        self.set_machine_state("READY")
        if total_result == "OK":
            self.result_label.setStyleSheet(
                "background-color:green;color:white;font-size:20px;"
            )
        else:
            self.result_label.setStyleSheet(
                "background-color:red;color:white;font-size:20px;"
            )
        self.log_box.clear()
        for msg in message:
            self.log_box.append(msg)
        self.update_alarm_display()
        self.update_oee()
        #print("\n".join(message))
    
    def assign_tools(self):
        self.tool_manager.clear()
        roi_count = len(
            self.camera_widget.roi_list
        )
        if roi_count >= 1:
            self.tool_manager.add_tool(0,"pattern")
            self.tool_manager.add_tool(0,"ocr")
        if roi_count >= 2:
            self.tool_manager.add_tool(1,"presence")
            self.tool_manager.add_tool(1,"brightness")
        if roi_count >= 3:
            self.tool_manager.add_tool(2,"pattern")
        print("TOOLS:",self.tool_manager.roi_tools)
    
    def show_tools(self):
        print(self.tool_manager.roi_tools)

    def ocr_check(self):
        if not hasattr(self,"current_frame"):
            return
        crop = self.camera_widget.get_roi_image(self.current_frame,0)
        if crop is None:
            return
        result = self.ocr_tool.inspect(crop)
        print(result)
        if isinstance(result, dict):
            self.result_label.setText(result.get("text",""))
        else:
            self.result_label.setText(str(result))
    
    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.auto_btn.setText("Stop Auto")
            self.auto_timer.start(500)  # 0.5 sec
        else:
            self.auto_btn.setText("Start Auto")
            self.auto_timer.stop()

    def auto_inspect(self):
        if not self.auto_mode:
            return
        if self.machine_state != "READY":
            return
        if not self.plc.read_trigger():
            return
        self.set_machine_state("BUSY")
        self.cycle_start_time = time.time()
        self.plc.set_trigger(False)
        self.inspect_all()

    def fake_trigger(self):
        self.plc.set_trigger(True)
    
    def test_plc(self):
        self.plc.write_ok()
        self.log_box.append("PLC OK SENT")
        self.plc.write_ng()
        self.log_box.append("PLC NG SENT")
    
    def refresh_recipe_list(self):
        import os
        self.recipe_list.clear()
        if not os.path.exists("recipes"):
            return
        for file in os.listdir("recipes"):
            if file.endswith(".json"):
                self.recipe_list.addItem(file.replace(".json", ""))
    
    def recipe_selected(self, name):
        self.recipe_name.setText(name)
        if name:
            self.load_recipe()
    
    def update_permission(self):
        role = self.current_role
        is_engineer = (
            role == "Engineer"
            or role == "Admin"
        )
        is_admin = (role == "Admin")
        self.save_recipe_btn.setEnabled(is_engineer)
        self.master_btn.setEnabled(is_engineer)
        self.assign_btn.setEnabled(is_engineer)
        self.add_user_btn.setEnabled(is_admin)
        self.delete_user_btn.setEnabled(is_admin)
        self.change_password_btn.setEnabled(is_admin)
    
    def login(self):
        from PyQt5.QtWidgets import (QInputDialog)
        username, ok = (
            QInputDialog.getText(self,"Login","Username"))
        if not ok:
            return
        password, ok = (
            QInputDialog.getText(self,"Login","Password"))
        if not ok:
            return
        role = (
            self.user_manager.login(username,password))
        if role is None:
            self.log_box.append("LOGIN FAILED")
            return
        self.current_role = role
        self.current_user = {"username": username,"role": role}
        self.user_label.setText(f"USER : {username}")
        self.role_label.setText(f"ROLE : {role}")
        self.update_permission()
        self.log_box.append(f"LOGIN : {role}")
        self.audit_logger.write(username,"LOGIN")
    
    def logout(self):
        username = self.current_user["username"]
        self.audit_logger.write(username,"LOGOUT")
        self.current_user = {"username": "GUEST","role": "operator"}
        self.current_role = "operator"
        self.user_label.setText("USER : GUEST")
        self.role_label.setText("ROLE : operator")
        self.update_permission()
        self.log_box.append("LOGOUT")
    
    def add_user(self):
        username, ok = QInputDialog.getText(self,"Add User","Username")
        if not ok:
            return
        password, ok = QInputDialog.getText(self,"Add User","Password")
        if not ok:
            return
        role, ok = QInputDialog.getItem(self,"Role","Select Role",
            [
                "Operator",
                "Engineer",
                "Admin"
            ],0,False)
        if not ok:
            return
        result = self.user_manager.add_user(
            username,
            password,
            role
        )
        if result:
            self.log_box.append(
                f"USER CREATED : {username}"
            )
        else:
            self.log_box.append(
                "USER EXISTS"
            )
        self.audit_logger.write(
        self.current_user["username"],f"ADD_USER:{username}")
    
    def delete_user(self):
        users = list(self.user_manager.users.keys())
        if "admin" in users:
            users.remove("admin")
        if len(users) == 0:
            self.log_box.append("NO USER")
            return
        username, ok = QInputDialog.getItem(self,"Delete User","Select User",users,0,False)
        if not ok:
            return
        result = self.user_manager.delete_user(username)
        if result:
            self.log_box.append(f"USER DELETED : {username}")
        else:
            self.log_box.append("DELETE FAILED")
        self.audit_logger.write(self.current_user["username"],f"DELETE_USER:{username}")
    
    def change_password(self):
        users = list(self.user_manager.users.keys())
        username, ok = QInputDialog.getItem(self,"Change Password","Select User",users,0,False)
        if not ok:
            return
        password, ok = QInputDialog.getText(self,"Change Password","New Password")
        if not ok:
            return
        result = self.user_manager.change_password(username,password)
        if result:
            self.log_box.append(f"PASSWORD CHANGED : {username}")
        else:
            self.log_box.append(
                "CHANGE FAILED"
            )

    def show_audit_log(self):
        try:
            with open(
                "audit_log.txt",
                "r",
                encoding="utf-8"
            ) as f:
                data = f.read()
            self.log_box.clear()
            self.log_box.setPlainText(data)
        except Exception as e:
            self.log_box.append(f"AUDIT LOG ERROR : {e}")
    
    def show_history(self):
        rows = self.database.get_all()
        self.history_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                self.history_table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(
                        str(value)))
    
    def filter_history(self, value):
        if value == "ALL":
            rows = self.database.get_all()
        else:
            rows = self.database.search_result(value)
        self.history_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, item in enumerate(row):
                self.history_table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(
                        str(item)))
    
    def search_recipe_history(self):
        recipe = self.recipe_name.text()
        rows = self.database.search_recipe(recipe)
        self.history_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, item in enumerate(row):
                self.history_table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(
                        str(item)))
    
    def history_row_clicked(self,row,column):
        item = self.history_table.item(row,6)
        if item is None:
            return
        image_path = item.text()
        from PyQt5.QtGui import QPixmap
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.log_box.append(f"IMAGE NOT FOUND : {image_path}")
            return
        self.image_preview.setPixmap(
            pixmap.scaled(250,250))
    
    def export_csv(self):
        rows = self.database.get_all()
        import csv
        with open(
            "inspection_history.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
            [
                "ID",
                "DATETIME",
                "RECIPE",
                "RESULT",
                "REASON",
                "SCORE",
                "IMAGE"
            ]
            )
            for row in rows:
                writer.writerow(row)
        self.log_box.append("CSV EXPORTED")
    
    def export_pdf(self):
        rows = self.database.get_all()
        pdf = SimpleDocTemplate("Inspection_Report.pdf")
        styles = getSampleStyleSheet()
        content = []
        content.append(
            Paragraph("Vision Inspection Report",styles["Title"]))
        content.append(
            Spacer(1,20))
        for row in rows[-20:]:
            content.append(
                Paragraph(f"Date : {row[1]}",styles["Normal"]))
            content.append(
                Paragraph(f"Recipe : {row[2]}",styles["Normal"]))
            content.append(
                Paragraph(f"Result : {row[3]}",styles["Normal"]))
            content.append(
                Paragraph(f"Reason : {row[4]}",styles["Normal"]))
            content.append(
                Paragraph(f"Score : {row[5]}",styles["Normal"]))
            image_path = row[6]
            import os
            if image_path and os.path.exists(image_path):
                content.append(
                    Image(image_path,width=120,height=120))
            content.append(Spacer(1,15))
        pdf.build(content)
        self.log_box.append("PDF EXPORTED")

    def show_trend(self):
        rows = self.database.get_last_results(50)
        rows.reverse()
        data = []
        for row in rows:
            if row[0] == "OK":
                data.append(1)
            else:
                data.append(0)
        plt.figure(figsize=(8,4))
        plt.plot(data,marker="o")
        plt.title("Inspection Trend")
        plt.xlabel("Inspection")
        plt.ylabel("OK=1  NG=0")
        plt.grid(True)
        plt.show()
    
    def set_machine_state(self,state):
        self.machine_state = state
        self.machine_label.setText(
            f"STATE : {state}"
        )
        if state == "READY":
            self.machine_label.setStyleSheet(
                "background-color:green;color:white;"
            )
        elif state == "BUSY":
            self.machine_label.setStyleSheet(
                "background-color:orange;color:black;"
            )
        elif state == "OK":
            self.machine_label.setStyleSheet(
                "background-color:blue;color:white;"
            )
        elif state == "NG":
            self.machine_label.setStyleSheet(
                "background-color:red;color:white;"
            )
    
    def update_alarm_display(self):
        self.alarm_label.setText(
            f"PATTERN : {self.alarm_counter['NG_PATTERN']}\n"
            f"PRESENCE : {self.alarm_counter['NG_PRESENCE']}\n"
            f"OCR : {self.alarm_counter['NG_OCR']}\n"
            f"BRIGHT : {self.alarm_counter['NG_BRIGHTNESS']}\n"
            f"TIMEOUT : {self.alarm_counter['TIMEOUT']}"
        )
    
    def update_oee(self):
        if self.total_runtime <= 0:
            return
        availability = (
            self.total_cycle
            /
            self.total_runtime
        ) * 100
        performance = (
            self.ideal_cycle_time
            /
            max(self.last_cycle_time,1)
        ) * 100
        quality = (
            self.good_count
            /
            max(self.total_cycle,1)
        ) * 100
        oee = (
            availability
            * performance
            * quality
        ) / 10000
        self.oee_label.setText(
            f"A : {availability:.1f}%\n"
            f"P : {performance:.1f}%\n"
            f"Q : {quality:.1f}%\n"
            f"OEE : {oee:.1f}%"
        )
    def set_reference(self):
        if not hasattr(self, "current_frame"):
            return
        crop = self.camera_widget.get_roi_image(
            self.current_frame,
            0
        )
        if crop is None:
            return
        self.pattern_manager.save_master(
            "reference",
            crop
        )
        roi = self.camera_widget.roi_list[0]

        frame_h, frame_w = self.current_frame.shape[:2]

        widget_w = self.camera_widget.width()
        widget_h = self.camera_widget.height()

        scale_x = frame_w / widget_w
        scale_y = frame_h / widget_h

        self.reference_x = int(roi.x() * scale_x)
        self.reference_y = int(roi.y() * scale_y)
        print(
            f"REFERENCE SAVED FRAME POS = "
            f"{self.reference_x},{self.reference_y}"
        )
        self.log_box.append(
            f"REFERENCE SAVED ({self.reference_x},{self.reference_y})"
        )

    
    def get_reference_offset(self):

        if not hasattr(self, "reference_x"):
            return 0,0

        if not hasattr(self, "reference_y"):
            return 0,0

        print(
            f"REFERENCE POS = "
            f"{self.reference_x},"
            f"{self.reference_y}"
        )
        
        master = self.pattern_manager.load_master(
            "reference"
        )

        if master is None:
            return 0,0

        ok, dx, dy, score = (
            self.reference_tool.find_offset(
                self.current_frame,
                master,
                self.reference_x,
                self.reference_y
            )
        )

        print(
            f"REFERENCE DX={dx} DY={dy} SCORE={score:.1f}"
        )

        if score < 90:
            print("REFERENCE NOT FOUND")
            return 0,0

        return dx,dy