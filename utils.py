"""
Utility functions for drowsiness detection.
"""

import cv2
import numpy as np
from scipy.spatial import distance as dist
import logging
import os
from typing import Tuple, List


def setup_logging(log_level: str = "INFO", log_file: str = "app.log") -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def eye_aspect_ratio(eye_points: np.ndarray) -> float:
    """
    Calculate the eye aspect ratio (EAR) given eye landmark points.
    
    Args:
        eye_points: Array of 6 (x, y) coordinates for eye landmarks
        
    Returns:
        Eye aspect ratio value
    """
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    
    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye_points[0], eye_points[3])
    
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear


def draw_eye_landmarks(frame: np.ndarray, eye_points: np.ndarray, color: Tuple[int, int, int] = (0, 255, 0)) -> None:
    """
    Draw eye landmarks on the frame.
    
    Args:
        frame: Input image frame
        eye_points: Array of eye landmark points
        color: BGR color tuple for drawing
    """
    hull = cv2.convexHull(eye_points)
    cv2.drawContours(frame, [hull], -1, color, 1)


def draw_status_text(frame: np.ndarray, text: str, position: Tuple[int, int], 
                    color: Tuple[int, int, int] = (255, 255, 255)) -> None:
    """
    Draw status text on the frame.
    
    Args:
        frame: Input image frame
        text: Text to display
        position: (x, y) position for text
        color: BGR color tuple for text
    """
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def check_model_file(model_path: str) -> bool:
    """
    Check if the facial landmark model file exists.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        True if file exists, False otherwise
    """
    if not os.path.exists(model_path):
        print(f"Error: Facial landmark model file not found at {model_path}")
        print("Please download the model from:")
        print("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        print("Extract it and place it in the project directory.")
        return False
    return True


def create_alarm_sound() -> None:
    """Create a simple alarm sound file if it doesn't exist."""
    alarm_file = "alarm.wav"
    if not os.path.exists(alarm_file):
        print(f"Creating default alarm sound: {alarm_file}")
        # This would typically use a library to generate a simple beep
        # For now, we'll just create a placeholder
        with open(alarm_file, 'w') as f:
            f.write("# Placeholder for alarm sound file\n")
            f.write("# Replace this with an actual .wav file for audio alerts\n")


def get_face_landmarks_indices() -> Tuple[List[int], List[int]]:
    """
    Get the facial landmark indices for left and right eyes.
    
    Returns:
        Tuple of (left_eye_indices, right_eye_indices)
    """
    # Facial landmark indices for eyes based on 68-point model
    left_eye_start, left_eye_end = 42, 48
    right_eye_start, right_eye_end = 36, 42
    
    left_eye_indices = list(range(left_eye_start, left_eye_end))
    right_eye_indices = list(range(right_eye_start, right_eye_end))
    
    return left_eye_indices, right_eye_indices