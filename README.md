# Driver Drowsiness Detection System

A real-time AI-powered system that monitors driver alertness using computer vision and facial landmark detection to prevent accidents caused by driver fatigue.

## Features

- **Real-time Eye Monitoring**: Uses Eye Aspect Ratio (EAR) calculation to detect closed eyes
- **Facial Landmark Detection**: Employs dlib's 68-point facial landmark model
- **Audio Alerts**: Plays alarm sounds when drowsiness is detected
- **Configurable Thresholds**: Adjustable sensitivity settings
- **Production Ready**: Comprehensive logging, error handling, and modular design
- **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.7+
- Webcam/Camera
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the facial landmark model**:
   - Download `shape_predictor_68_face_landmarks.dat.bz2` from:
     http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract the file and place `shape_predictor_68_face_landmarks.dat` in the project directory

4. **Add an alarm sound file** (optional):
   - Place a `.wav` file named `alarm.wav` in the project directory
   - The system will create a placeholder file if none is provided

## Usage

1. **Run the system**:
   ```bash
   python main.py
   ```

2. **System Controls**:
   - **Look at the camera** to start monitoring
   - **Press 'q'** to quit the application
   - **Press 's'** to save the current frame
   - **Keep your eyes open** to maintain "Driver Alert" status

3. **Status Indicators**:
   - **Green "Driver Alert"**: Normal, alert state
   - **Yellow "Eyes closed: X/Y"**: Eyes detected as closed, counting frames
   - **Red "DROWSINESS ALERT!"**: Alert triggered, audio alarm activated

## Configuration

Edit `config.py` to customize the system:

```python
# Key settings
EAR_THRESHOLD = 0.25          # Lower = more sensitive
EAR_CONSEC_FRAMES = 20        # Frames before alert (lower = faster alert)
FRAME_WIDTH = 640             # Camera resolution
FRAME_HEIGHT = 480
ALARM_ENABLED = True          # Enable/disable audio alerts
```

## How It Works

1. **Face Detection**: Uses dlib's HOG-based face detector
2. **Landmark Extraction**: Identifies 68 facial landmarks, focusing on eyes
3. **EAR Calculation**: Computes Eye Aspect Ratio using eye landmark geometry
4. **Drowsiness Detection**: Monitors EAR values over consecutive frames
5. **Alert System**: Triggers visual and audio alerts when drowsiness is detected

### Eye Aspect Ratio (EAR) Formula

```
EAR = (|p2 - p6| + |p3 - p5|) / (2 * |p1 - p4|)
```

Where p1-p6 are the eye landmark points. EAR decreases significantly when eyes are closed.

## File Structure

```
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── shape_predictor_68_face_landmarks.dat  # Facial landmark model (download required)
├── alarm.wav           # Audio alert file (optional)
└── drowsiness_detection.log  # System logs
```

## Troubleshooting

### Common Issues

1. **"No face detected"**: 
   - Ensure good lighting
   - Position face clearly in camera view
   - Check camera permissions

2. **"Facial landmark model file not found"**:
   - Download the model file as described in installation
   - Verify file name and location

3. **Camera not working**:
   - Check camera index in config.py (try 0, 1, 2...)
   - Ensure no other application is using the camera

4. **No audio alerts**:
   - Install playsound: `pip install playsound`
   - Add a valid .wav file as alarm.wav
   - Check audio system permissions

### Performance Optimization

- Reduce frame size in config.py for better performance
- Adjust EAR_CONSEC_FRAMES for faster/slower detection
- Close other applications to free up system resources

## Safety Notice

This system is designed as a safety aid and should not be the sole method of preventing drowsy driving. Always ensure you are well-rested before driving and take regular breaks during long trips.

## License

This project is provided for educational and safety purposes. Use responsibly and in accordance with local traffic laws and regulations.