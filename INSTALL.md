# 📦 Installation Guide - Vision Platform Enterprise v2.0

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.14+
- **Python**: 3.7 or higher
- **RAM**: 4GB (8GB recommended for multi-camera)
- **Storage**: 500MB for installation + space for image storage
- **Processor**: Intel i5 or equivalent

### Camera Requirements
- USB 2.0 or USB 3.0 cameras
- Supported: Most standard USB webcams
- Resolution: 640x480 to 4K (depending on performance)

### PLC Requirements (Optional)
- Ethernet connection to PLC
- IP address configuration
- Modbus TCP support (recommended)

---

## Step 1: Python Installation

### Windows
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### macOS
```bash
brew install python3
python3 --version
```

---

## Step 2: Clone Repository

### Using Git
```bash
git clone https://github.com/theerawoot1478-sudo/VisionPlatform.git
cd VisionPlatform
```

### Or Download ZIP
1. Go to: https://github.com/theerawoot1478-sudo/VisionPlatform
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open terminal in that directory

---

## Step 3: Create Virtual Environment (Recommended)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal.

---

## Step 4: Install Dependencies

### Core Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Optional Dependencies (AI/Deep Learning)
```bash
pip install -r requirements_optional.txt
```

### Install Tesseract for OCR

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default path: `C:\Program Files\Tesseract-OCR`)
3. Add to config.yaml:
   ```yaml
   ocr:
     tesseract_path: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   ```

**Linux:**
```bash
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

---

## Step 5: Configure System

### Edit config.yaml

1. Open `config.yaml` in text editor
2. Configure cameras:
   ```yaml
   camera:
     max_cameras: 4
     cameras:
       - id: 0
         name: "Camera 1"
         enabled: true  # Change to true to enable
   ```

3. Configure PLC (if needed):
   ```yaml
   plc:
     enabled: true
     host: "192.168.1.100"  # Your PLC IP
     port: 502
   ```

4. Save file

---

## Step 6: Verify Installation

### Check Python Packages
```bash
pip list
```

Should include:
- opencv-python
- PyQt5
- numpy
- PyYAML

### Check Camera Access
```bash
python -c "import cv2; print([i for i in range(5) if cv2.VideoCapture(i).isOpened()])"
```

Example output: `[0]` means 1 camera detected at index 0

### Check Config
```bash
python -c "from core.config_manager import ConfigManager; c = ConfigManager(); c.display_config()"
```

---

## Step 7: Run Application

### Start Vision Platform
```bash
python main.py
```

Expected output:
```
============================================================
🎥 VISION PLATFORM ENTERPRISE v2.0
Advanced Vision Inspection System
============================================================

✅ Directory ready: database
✅ Directory ready: recipes
...
✅ Application started successfully
```

### Access GUI
Application window should appear. Default login:
- **Username**: `admin`
- **Password**: `1234`
- **Role**: Admin

---

## Troubleshooting

### Issue: Module not found
```
ModuleNotFoundError: No module named 'cv2'
```
**Solution:**
```bash
pip install opencv-python
```

### Issue: Python version incompatible
```
SyntaxError: invalid syntax
```
**Solution:**
- Check Python version: `python --version`
- Upgrade: `python -m pip install --upgrade python`
- Requires Python 3.7+

### Issue: Camera not detected
```
❌ Cannot open camera 0
```
**Solution:**
1. Connect USB camera
2. Check in Device Manager (Windows) or `lsusb` (Linux)
3. Try: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Issue: PyQt5 GUI not appearing
```
QXcbConnection: Could not connect to display
```
**Solution (Linux with SSH):**
```bash
export DISPLAY=:0
python main.py
```

### Issue: PLC Connection Failed
```
❌ PLC Connection Error: Connection refused
```
**Solution:**
1. Verify PLC IP in config.yaml
2. Test: `ping 192.168.1.100`
3. Check PLC is powered on and network-connected
4. Verify port 502 (Modbus default)

### Issue: Low FPS / Performance Issues
**Solutions:**
1. Reduce camera resolution in config.yaml
2. Use fewer ROIs
3. Disable unused inspection tools
4. Check CPU usage: `Task Manager` (Windows) or `htop` (Linux)

### Issue: Permission Denied (Linux)
```
Permission denied: './venv/bin/activate'
```
**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## Post-Installation Setup

### 1. Create Your First Recipe
1. Start application
2. Draw ROIs on camera feed
3. Click "Set Master" to capture reference
4. Assign tools to ROIs
5. Save recipe with unique name

### 2. Test PLC Connection
1. Configure PLC settings in config.yaml
2. Click "PLC Test" button
3. Check console for connection status

### 3. Perform Test Inspection
1. Load recipe
2. Click "Inspect All"
3. Check results in history

---

## Uninstall

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

### Remove Application
```bash
rm -rf VisionPlatform
```

---

## Getting Help

### Documentation
- See README.md for overview
- See config.yaml for configuration options
- Check individual tool files for implementation details

### Report Issues
- GitHub Issues: https://github.com/theerawoot1478-sudo/VisionPlatform/issues
- Email: theerawoot1478@gmail.com

### Common Commands
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run tests
pytest tests/

# Generate logs
python main.py > debug.log 2>&1

# Check configuration
python -c "from core.config_manager import ConfigManager; ConfigManager().display_config()"
```

---

## Performance Tips

1. **Use dedicated GPU** for AI tools
2. **Disable DEBUG mode** in config.yaml for production
3. **Regular database backup** for inspection history
4. **Optimize camera resolution** based on requirements
5. **Use SSD** for image storage
6. **Monitor system resources** during operation

---

**Installation Complete! 🎉**

Start using Vision Platform:
```bash
python main.py
```
