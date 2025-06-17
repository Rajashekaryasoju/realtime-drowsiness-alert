# Driver Drowsiness Detection System - Complete Setup Guide

## System Requirements

### Python Version
- **Required**: Python 3.7 or higher
- **Recommended**: Python 3.8 to 3.11
- **Best Performance**: Python 3.9 or 3.10

### Hardware Requirements
- **Camera**: Built-in webcam or external USB camera
- **RAM**: Minimum 4GB (8GB recommended)
- **CPU**: Any modern processor (Intel i3/AMD equivalent or better)
- **OS**: Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+

## Step-by-Step Installation

### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.7+ (e.g., Python 3.9.7)
```

If Python is not installed:
- **Windows**: Download from https://python.org/downloads/
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: `sudo apt update && sudo apt install python3 python3-pip`

### Step 2: Install System Dependencies

#### Windows:
```bash
# Install Visual Studio Build Tools (required for dlib)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# OR install Visual Studio Community with C++ workload

# Install CMake
pip install cmake
```

#### macOS:
```bash
# Install Xcode command line tools
xcode-select --install

# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install cmake
brew install cmake
```

#### Linux (Ubuntu/Debian):
```bash
# Update package list
sudo apt update

# Install required system packages
sudo apt install -y python3-pip python3-dev build-essential cmake
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libboost-all-dev
```

### Step 3: Create Project Directory

```bash
# Create and navigate to project directory
mkdir drowsiness-detection
cd drowsiness-detection
```

### Step 4: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv drowsiness_env

# Activate virtual environment
# Windows:
drowsiness_env\Scripts\activate
# macOS/Linux:
source drowsiness_env/bin/activate

# Your prompt should now show (drowsiness_env)
```

### Step 5: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages one by one for better error handling
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install scipy==1.11.1
pip install cmake==3.27.0

# Install dlib (this may take 5-10 minutes)
pip install dlib==19.24.2

# Install remaining packages
pip install imutils==0.5.4
pip install playsound==1.3.0
```

**Alternative - Install all at once:**
```bash
pip install -r requirements.txt
```

### Step 6: Download Facial Landmark Model

```bash
# Download the model file (68MB)
curl -O http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

# Extract the file
# Windows (using 7-Zip or WinRAR):
# Right-click → Extract Here

# macOS/Linux:
bunzip2 shape_predictor_68_face_landmarks.dat.bz2

# Verify the file exists
ls -la shape_predictor_68_face_landmarks.dat
```

**Manual Download (if curl fails):**
1. Go to: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
2. Download the file
3. Extract using your system's archive tool
4. Place `shape_predictor_68_face_landmarks.dat` in the project directory

### Step 7: Test Camera Access

```bash
# Quick camera test
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

### Step 8: Run the System

```bash
# Start the drowsiness detection system
python main.py
```

## Usage Instructions

### System Controls
- **Look at camera**: System starts monitoring automatically
- **Press 'q'**: Quit the application
- **Press 's'**: Save current frame as image
- **Keep eyes open**: Maintain "Driver Alert" status

### Status Indicators
- 🟢 **"Driver Alert"**: Normal, awake state
- 🟡 **"Eyes closed: X/20"**: Counting closed-eye frames
- 🔴 **"DROWSINESS ALERT!"**: Alert triggered, alarm playing

### Expected Behavior
1. **Face Detection**: Green rectangles around detected faces
2. **Eye Tracking**: Green outlines around eyes
3. **EAR Display**: Real-time Eye Aspect Ratio values
4. **Alert System**: Audio and visual warnings when drowsy

## Troubleshooting

### Common Issues and Solutions

#### 1. "No module named 'cv2'"
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

#### 2. "dlib installation failed"
**Windows:**
```bash
# Install Visual C++ Build Tools first
# Then try:
pip install --upgrade setuptools wheel
pip install dlib
```

**macOS:**
```bash
brew install boost
pip install dlib
```

**Linux:**
```bash
sudo apt install libboost-all-dev
pip install dlib
```

#### 3. "No face detected"
- **Check lighting**: Ensure good, even lighting on face
- **Camera position**: Face should be clearly visible and centered
- **Camera permissions**: Allow camera access in system settings
- **Try different camera**: Change `CAMERA_INDEX` in config.py (0, 1, 2...)

#### 4. "Facial landmark model file not found"
```bash
# Re-download the model
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

#### 5. "No audio alerts"
```bash
# Install audio dependencies
# Windows:
pip install playsound==1.2.2

# macOS:
pip install playsound pyobjc

# Linux:
sudo apt install python3-pyaudio
pip install playsound
```

#### 6. Camera not working
```bash
# Test different camera indices
python -c "
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f'Camera {i}: Available')
        cap.release()
    else:
        print(f'Camera {i}: Not available')
"
```

### Performance Optimization

#### For slower computers:
```python
# Edit config.py
FRAME_WIDTH = 320      # Reduce from 640
FRAME_HEIGHT = 240     # Reduce from 480
EAR_CONSEC_FRAMES = 15 # Reduce from 20
```

#### For faster detection:
```python
# Edit config.py
EAR_CONSEC_FRAMES = 10 # Reduce from 20
EAR_THRESHOLD = 0.3    # Increase from 0.25
```

## Configuration Options

### Key Settings in config.py

```python
# Sensitivity (lower = more sensitive)
EAR_THRESHOLD = 0.25

# Alert delay (lower = faster alerts)
EAR_CONSEC_FRAMES = 20

# Performance (lower = faster processing)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Features
ALARM_ENABLED = True
SHOW_LANDMARKS = True
SHOW_EAR_VALUES = True
```

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Camera Feed   │───▶│  Face Detection  │───▶│  Eye Tracking   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Audio Alert    │◀───│ Drowsiness Logic │◀───│ EAR Calculation │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Safety Notice

⚠️ **Important**: This system is a safety aid, not a replacement for:
- Adequate rest before driving
- Regular breaks during long trips
- Professional medical advice for sleep disorders
- Following traffic laws and regulations

## Next Steps

1. **Test the system** in good lighting conditions
2. **Calibrate settings** based on your face/eye characteristics
3. **Practice using** the controls before actual use
4. **Consider integration** with vehicle systems (advanced)

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all dependencies are installed
3. Test camera and audio separately
4. Check system logs in `drowsiness_detection.log`

---

**System Status Check:**
```bash
# Run this to verify everything is working
python -c "
import cv2, dlib, numpy, scipy, playsound
print('✅ All dependencies imported successfully')
print('✅ System ready to run')
"
```