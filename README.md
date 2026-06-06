# 📷 Vision Platform Enterprise v2.0

**Advanced Vision Inspection System with Multi-Camera Support and AI-Powered Quality Control**

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 Overview

**VisionPlatform** is a professional-grade vision inspection system designed for automated quality control in manufacturing. It supports multiple USB cameras (1-4), PLC integration via TCP/IP and Modbus, and multiple inspection tools for comprehensive product quality assessment.

### Key Features

- 🎥 **Multi-Camera Support**: Connect 1-4 USB cameras simultaneously
- 🤖 **AI-Powered Inspection**: Pattern recognition, OCR, color detection, blob analysis
- 🔌 **PLC Integration**: TCP/IP and Modbus protocol support
- 📊 **Real-time Dashboard**: Live monitoring, statistics, OEE tracking
- 🧮 **7 Inspection Tools**: Pattern, Presence, Brightness, OCR, Color, Blob, Measurement
- 👥 **User Management**: Role-based access control (Admin, Engineer, Operator)
- 📈 **Data Export**: CSV, PDF reports with trend analysis
- ⚙️ **Flexible Configuration**: YAML-based settings management
- 🔒 **Audit Logging**: Complete activity tracking

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VISION PLATFORM                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📷 USB Cameras (1-4)  ──→  MultiCameraManager             │
│     ├─ Camera 0                                            │
│     ├─ Camera 1                                            │
│     ├─ Camera 2                                            │
│     └─ Camera 3                                            │
│         ↓                                                   │
│  ┌─────────────────────────────────────┐                  │
│  │   INSPECTION ENGINE (Core Logic)    │                  │
│  │  • Recipe Management                 │                  │
│  │  • ROI Definition & Tracking         │                  │
│  │  • Tool Assignment                   │                  │
│  └─────────────────────────────────────┘                  │
│         ↓                                                   │
│  🛠️  INSPECTION TOOLS:                                    │
│     ├─ Pattern Matching (Template compare)               │
│     ├─ Presence Detection (Object existence)             │
│     ├─ Brightness Analysis (Illumination check)          │
│     ├─ OCR (Text recognition)                            │
│     ├─ Color Detection (HSV/RGB analysis)                │
│     ├─ Blob Analysis (Defect detection)                  │
│     └─ Measurement (Dimension check)                     │
│         ↓                                                   │
│  📊 DATA LAYER:                                           │
│     ├─ SQLite Database (Results history)                 │
│     ├─ Image Logger (Capture storage)                    │
│     ├─ Audit Logger (Activity tracking)                  │
│     └─ Statistics (Performance metrics)                  │
│         ↓                                                   │
│  🔌 PLC INTERFACE:                                        │
│     ├─ TCP/IP Socket                                     │
│     ├─ Modbus TCP/RTU                                    │
│     └─ Signal Mapping (OK/NG/Ready/Busy)                │
│         ↓                                                   │
│  🖥️  GUI (PyQt5):                                         │
│     ├─ Live camera feed                                  │
│     ├─ Recipe builder                                    │
│     ├─ Inspection results                                │
│     ├─ History & Statistics                              │
│     └─ User management                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, Linux, macOS
- **Dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

### Key Dependencies
- `opencv-python` - Image processing
- `PyQt5` - GUI framework
- `numpy` - Numerical computing
- `pyyaml` - Configuration management
- `reportlab` - PDF generation
- `pytesseract` - OCR engine

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/theerawoot1478-sudo/VisionPlatform.git
cd VisionPlatform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure System
Edit `config.yaml` to set your system parameters:
```yaml
camera:
  max_cameras: 4
  cameras:
    - id: 0
      name: "Camera 1"
      enabled: true
      exposure: 100

plc:
  enabled: true
  type: "tcp"
  host: "192.168.1.100"
  port: 502
```

### 4. Run Application
```bash
python main.py
```

---

## 📚 Usage Guide

### Starting the Application
```bash
python main.py
```

### Basic Workflow

#### 1. **Camera Setup**
- Connect 1-4 USB cameras
- Enable in `config.yaml`
- Click "Camera Status" to verify

#### 2. **Define Inspection Recipe**
- Draw ROIs (Regions of Interest) on camera feed
- Assign inspection tools to each ROI
- Set tool parameters (thresholds, calibration)
- Save recipe with unique name

#### 3. **Set Master References**
- Capture good product image
- Click "Set Master" to store reference
- Used for pattern matching

#### 4. **Run Inspection**
- Click "Inspect All" for single inspection
- Click "Start Auto" for continuous mode
- PLC signals OK/NG results

#### 5. **Monitor Results**
- View live results on dashboard
- Check OEE (Overall Equipment Effectiveness)
- Monitor alarm counters
- Track cycle time

### Inspection Tools

#### **Pattern Matching**
- Template-based product verification
- Threshold: 0-100 (matching score)
- Best for: Fixed product shapes

#### **Presence Detection**
- Checks if object exists in ROI
- Threshold: 0-100 (sensitivity)
- Best for: Component verification

#### **Brightness Analysis**
- Illumination level checking
- Range: 0-255 (min-max)
- Best for: Print quality, surface finish

#### **OCR (Optical Character Recognition)**
- Reads text from image
- Language: English/Multiple
- Best for: Date codes, serial numbers

#### **Color Detection**
- HSV/RGB color space analysis
- Threshold: Configurable
- Best for: Color verification, paint check

#### **Blob Analysis**
- Detects defects/particles
- Min/Max area, threshold configurable
- Best for: Scratch, dirt, defect detection

#### **Measurement**
- Dimension verification
- Requires calibration with reference
- Best for: Size inspection, gap measurement

---

## 🔧 Configuration

### config.yaml Structure
```yaml
app:
  name: "Vision Platform Enterprise"
  version: "2.0.0"
  debug: true

camera:
  max_cameras: 4
  default_camera_count: 1
  cameras:
    - id: 0
      name: "Camera 1"
      enabled: true
      exposure: 100
      gain: 1.0

plc:
  enabled: true
  type: "tcp"  # tcp, modbus_tcp
  host: "192.168.1.100"
  port: 502
  signals:
    trigger_input: "I0.0"
    ok_output: "Q0.0"
    ng_output: "Q0.1"

tools:
  pattern:
    threshold: 80
  presence:
    threshold: 20
  brightness:
    min_value: 50
    max_value: 200
  # ... more tools
```

---

## 📊 Database Schema

### inspection_history table
```sql
CREATE TABLE inspection_history(
    id INTEGER PRIMARY KEY,
    datetime TEXT,
    recipe TEXT,
    result TEXT,  -- OK/NG
    reason TEXT,  -- Why it's NG
    score REAL,   -- Confidence 0-100
    image_path TEXT
)
```

---

## 👥 User Roles

| Role | Permissions |
|------|------------|
| **Admin** | All operations, user management, system settings |
| **Engineer** | Create/edit recipes, set master, tool assignment |
| **Operator** | Run inspection, view results, basic monitoring |

### Default Users
- Username: `admin` | Password: `1234` | Role: Admin

---

## 🔌 PLC Integration

### Supported Protocols
- **TCP/IP**: Direct socket connection
- **Modbus TCP**: Standard industrial protocol
- **Modbus RTU**: Serial communication (with adapter)

### Signal Mapping Example
```yaml
signals:
  trigger_input: "I0.0"      # Input from PLC
  ok_output: "Q0.0"          # Output: Part is OK
  ng_output: "Q0.1"          # Output: Part is NG
  ready_output: "Q0.2"       # Output: System ready
  busy_output: "Q0.3"        # Output: System busy
```

### Testing PLC Connection
1. Configure PLC settings in `config.yaml`
2. Click "PLC Test" button
3. Check console output for connection status

---

## 📈 OEE Calculation

**OEE (Overall Equipment Effectiveness)** = Availability × Performance × Quality

```
Availability = Total Cycles / Total Runtime
Performance = Ideal Cycle Time / Actual Cycle Time
Quality = Good Count / Total Count
OEE = (Availability × Performance × Quality) / 100
```

---

## 🐛 Troubleshooting

### Camera Not Detected
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(5) if cv2.VideoCapture(i).isOpened()])"
```

### PLC Connection Failed
- Verify IP address and port in `config.yaml`
- Check network connectivity: `ping 192.168.1.100`
- Ensure PLC is powered and configured

### OCR Not Working
```bash
# Install Tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
```

### Low FPS on Multi-Camera
- Reduce camera resolution
- Lower inspection tool complexity
- Use fewer ROIs
- Check CPU usage

---

## 📁 Project Structure

```
VisionPlatform/
├── main.py                          # Application entry point
├── config.yaml                      # Configuration file
├── requirements.txt                 # Python dependencies
│
├── core/
│   ├── camera_manager.py            # Single camera driver
│   ├── multi_camera_manager.py      # Multi-camera support
│   ├── plc_manager.py               # Basic PLC interface
│   ├── plc_manager_enhanced.py      # Advanced PLC (TCP/Modbus)
│   ├── recipe_manager.py            # Recipe CRUD operations
│   ├── database.py                  # SQLite operations
│   ├── user_manager.py              # User authentication
│   ├── config_manager.py            # YAML config handler
│   ├── audit_logger.py              # Activity tracking
│   ├── statistics.py                # Performance metrics
│   ├── image_logger.py              # Image storage
│   ├── tool_manager.py              # Tool assignment
│   └── reference_tool.py            # Position offset detection
│
├── tools/
│   ├── pattern_tool.py              # Template matching
│   ├── presence_tool.py             # Object detection
│   ├── brightness_tool.py           # Illumination check
│   ├── ocr_tool.py                  # Text recognition
│   ├── color_tool.py                # Color detection ✨ NEW
│   ├── blob_tool.py                 # Defect detection ✨ NEW
│   ├── measurement_tool.py          # Dimension check ✨ NEW
│   ├── pattern_manager.py           # Master image storage
│   └── reference_tool.py            # Reference tracking
│
├── ui/
│   ├── main_window.py               # Main GUI
│   ├── camera_widget.py             # Camera display
│   └── dialogs/                     # Dialog windows
│
├── database/
│   └── vision.db                    # SQLite database
│
├── recipes/                         # Recipe files (JSON)
│   └── recipe_01.json
│
├── images/                          # Inspection images
│   ├── OK/
│   └── NG/
│
└── masters/                         # Master reference images
    ├── master_0.jpg
    ├── master_1.jpg
    ├── reference.jpg
    └── ...
```

---

## 🎓 Example: Complete Inspection Workflow

```python
from core.config_manager import ConfigManager
from core.multi_camera_manager import MultiCameraManager
from core.plc_manager_enhanced import PLCManagerEnhanced
from core.recipe_manager import RecipeManager
from tools.pattern_tool import PatternTool
from tools.color_tool import ColorTool

# 1. Load configuration
config_mgr = ConfigManager("config.yaml")
cam_config = config_mgr.get("camera")
plc_config = config_mgr.get("plc")

# 2. Initialize cameras
camera_mgr = MultiCameraManager(cam_config)
camera_mgr.display_status()

# 3. Connect to PLC
plc = PLCManagerEnhanced(plc_config)
plc.connect()

# 4. Load recipe
recipe_mgr = RecipeManager()
recipe = recipe_mgr.load_recipe("Recipe_01")

# 5. Initialize tools
pattern_tool = PatternTool(threshold=80)
color_tool = ColorTool(method="HSV", threshold=50)

# 6. Inspect
for cam_id in camera_mgr.get_connected_cameras():
    ret, frame = camera_mgr.read_frame(cam_id)
    
    if ret:
        # Pattern inspection
        result1 = pattern_tool.inspect(frame)
        
        # Color inspection
        result2 = color_tool.inspect(frame)
        
        # Determine final result
        final = "OK" if (result1["result"] == "OK" and result2["result"] == "OK") else "NG"
        
        # Send to PLC
        if final == "OK":
            plc.write_ok()
        else:
            plc.write_ng()
```

---

## 📊 API Reference

### MultiCameraManager
```python
mgr = MultiCameraManager(config)
mgr.connect_camera(0)
ret, frame = mgr.read_frame(0)
cameras = mgr.get_connected_cameras()
mgr.release_all()
```

### PLCManagerEnhanced
```python
plc = PLCManagerEnhanced(config)
plc.connect()
trigger = plc.read_trigger()
plc.write_ok()
plc.write_ng()
plc.test_connection()
```

### PatternTool
```python
tool = PatternTool(threshold=80)
tool.set_master(master_image)
result = tool.inspect(image)  # Returns {'result', 'score'}
```

### ColorTool ✨ NEW
```python
tool = ColorTool(method="HSV", threshold=50)
tool.set_target_color((0, 255, 0))  # BGR format
result = tool.inspect(image)
```

### BlobTool ✨ NEW
```python
tool = BlobTool(min_area=50, max_area=50000)
result = tool.inspect(image)
defects = tool.detect_defects(image)
```

### MeasurementTool ✨ NEW
```python
tool = MeasurementTool(unit="mm", pixels_per_mm=10.0)
tool.calibrate(100, 10)  # 100 pixels = 10mm
result = tool.inspect(image, target_dimension=100)
```

---

## 🔐 Security Features

- ✅ Password hashing (SHA256)
- ✅ Role-based access control
- ✅ Audit logging of all operations
- ✅ User session management
- ✅ Configuration encryption support

---

## 🚀 Performance Optimization

### Tips for Better FPS
1. **Reduce Resolution**: Lower camera resolution in config.yaml
2. **ROI Optimization**: Use minimal ROIs
3. **Tool Selection**: Use faster tools (pattern > color > measurement)
4. **Multi-threading**: Inspection engine uses threaded processing
5. **Hardware**: Use dedicated GPU for AI tools

### Typical Performance
- Single Camera: 30+ FPS
- Dual Camera: 15+ FPS
- Quad Camera: 8+ FPS
- (Depends on tool complexity and hardware)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Theerawoot** - Vision Platform Developer
- GitHub: [@theerawoot1478-sudo](https://github.com/theerawoot1478-sudo)

---

## 📞 Support

For issues, questions, or suggestions:
- 🐛 [Report Bug](https://github.com/theerawoot1478-sudo/VisionPlatform/issues)
- 💡 [Request Feature](https://github.com/theerawoot1478-sudo/VisionPlatform/issues)
- 📧 Email: theerawoot1478@gmail.com

---

## 🎉 Version History

### v2.0.0 (Current)
- ✨ Added Multi-Camera Support (1-4 cameras)
- ✨ Added Enhanced PLC Manager (TCP/IP + Modbus)
- ✨ Added ColorTool, BlobTool, MeasurementTool
- ✨ Added ConfigManager (YAML configuration)
- 🐛 Fixed error handling throughout
- 📚 Complete documentation
- 🧹 Code optimization and cleanup

### v1.0.0
- Initial release with single camera
- Basic PLC support
- 4 inspection tools

---

**Made with ❤️ for Industrial Vision**
