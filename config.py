"""
Configuration settings for the drowsiness detection system.
"""

class Config:
    # Eye aspect ratio (EAR) threshold for drowsiness detection
    EAR_THRESHOLD = 0.25
    
    # Number of consecutive frames below threshold to trigger alert
    EAR_CONSEC_FRAMES = 20
    
    # Frame dimensions for processing (smaller = faster)
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    # Facial landmark predictor model path
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
    
    # Audio alert settings
    ALARM_SOUND = "alarm.wav"
    ALARM_ENABLED = True
    
    # Display settings
    SHOW_LANDMARKS = True
    SHOW_EAR_VALUES = True
    WINDOW_NAME = "Driver Drowsiness Detection"
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FILE = "drowsiness_detection.log"
    
    # Camera settings
    CAMERA_INDEX = 0
    FPS = 30