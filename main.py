"""
Driver Drowsiness Detection System

This system uses computer vision and facial landmark detection to monitor
driver alertness in real-time through webcam feed. It calculates the Eye
Aspect Ratio (EAR) to detect when eyes are closed for extended periods
and triggers audio alerts to prevent accidents due to driver fatigue.
"""

import cv2
import dlib
import numpy as np
import time
from threading import Thread
import logging
from typing import Optional

from config import Config
from utils import (
    setup_logging, eye_aspect_ratio, draw_eye_landmarks, 
    draw_status_text, check_model_file, create_alarm_sound,
    get_face_landmarks_indices
)

try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False
    print("Warning: playsound not available. Audio alerts disabled.")


class DrowsinessDetector:
    """Main class for drowsiness detection system."""
    
    def __init__(self):
        self.logger = setup_logging(Config.LOG_LEVEL, Config.LOG_FILE)
        self.frame_counter = 0
        self.alarm_on = False
        self.ear_values = []
        
        # Initialize face detector and landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = None
        
        # Eye landmark indices
        self.left_eye_indices, self.right_eye_indices = get_face_landmarks_indices()
        
        # Camera capture
        self.cap = None
        
        self.logger.info("Drowsiness Detection System initialized")
    
    def initialize_camera(self) -> bool:
        """Initialize camera capture."""
        try:
            self.cap = cv2.VideoCapture(Config.CAMERA_INDEX)
            if not self.cap.isOpened():
                self.logger.error("Failed to open camera")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, Config.FPS)
            
            self.logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing camera: {e}")
            return False
    
    def initialize_predictor(self) -> bool:
        """Initialize facial landmark predictor."""
        try:
            if not check_model_file(Config.PREDICTOR_PATH):
                return False
            
            self.predictor = dlib.shape_predictor(Config.PREDICTOR_PATH)
            self.logger.info("Facial landmark predictor initialized")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing predictor: {e}")
            return False
    
    def play_alarm(self) -> None:
        """Play alarm sound in a separate thread."""
        if not SOUND_AVAILABLE or not Config.ALARM_ENABLED:
            return
        
        def alarm_thread():
            try:
                playsound(Config.ALARM_SOUND)
            except Exception as e:
                self.logger.warning(f"Could not play alarm sound: {e}")
        
        if not self.alarm_on:
            self.alarm_on = True
            thread = Thread(target=alarm_thread)
            thread.daemon = True
            thread.start()
    
    def process_frame(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Process a single frame for drowsiness detection.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Processed frame with annotations
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 0)
        
        if len(faces) == 0:
            draw_status_text(frame, "No face detected", (10, 30), (0, 0, 255))
            self.frame_counter = 0
            self.alarm_on = False
            return frame
        
        for face in faces:
            # Get facial landmarks
            landmarks = self.predictor(gray, face)
            landmarks_np = np.array([[p.x, p.y] for p in landmarks.parts()])
            
            # Extract eye coordinates
            left_eye = landmarks_np[self.left_eye_indices]
            right_eye = landmarks_np[self.right_eye_indices]
            
            # Calculate EAR for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0
            
            # Store EAR values for averaging
            self.ear_values.append(ear)
            if len(self.ear_values) > 10:
                self.ear_values.pop(0)
            
            avg_ear = np.mean(self.ear_values)
            
            # Draw eye landmarks if enabled
            if Config.SHOW_LANDMARKS:
                draw_eye_landmarks(frame, left_eye, (0, 255, 0))
                draw_eye_landmarks(frame, right_eye, (0, 255, 0))
            
            # Check for drowsiness
            if avg_ear < Config.EAR_THRESHOLD:
                self.frame_counter += 1
                
                if self.frame_counter >= Config.EAR_CONSEC_FRAMES:
                    # Drowsiness detected
                    draw_status_text(frame, "DROWSINESS ALERT!", (10, 30), (0, 0, 255))
                    draw_status_text(frame, "Wake up!", (10, 70), (0, 0, 255))
                    
                    # Play alarm
                    self.play_alarm()
                    
                    self.logger.warning(f"Drowsiness detected! EAR: {avg_ear:.3f}")
                else:
                    draw_status_text(frame, f"Eyes closed: {self.frame_counter}/{Config.EAR_CONSEC_FRAMES}", 
                                   (10, 30), (0, 255, 255))
            else:
                self.frame_counter = 0
                self.alarm_on = False
                draw_status_text(frame, "Driver Alert", (10, 30), (0, 255, 0))
            
            # Display EAR values if enabled
            if Config.SHOW_EAR_VALUES:
                draw_status_text(frame, f"EAR: {avg_ear:.3f}", (10, frame.shape[0] - 20), (255, 255, 255))
                draw_status_text(frame, f"Threshold: {Config.EAR_THRESHOLD}", 
                               (10, frame.shape[0] - 50), (255, 255, 255))
        
        return frame
    
    def run(self) -> None:
        """Main execution loop."""
        self.logger.info("Starting drowsiness detection system...")
        
        # Initialize components
        if not self.initialize_predictor():
            return
        
        if not self.initialize_camera():
            return
        
        # Create alarm sound file if needed
        create_alarm_sound()
        
        print("\n" + "="*50)
        print("DRIVER DROWSINESS DETECTION SYSTEM")
        print("="*50)
        print("Instructions:")
        print("- Look at the camera to start monitoring")
        print("- Keep your eyes open and alert")
        print("- Press 'q' to quit the application")
        print("- Press 's' to save current frame")
        print("="*50 + "\n")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.error("Failed to read frame from camera")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                if processed_frame is not None:
                    # Display the frame
                    cv2.imshow(Config.WINDOW_NAME, processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.logger.info("Quit command received")
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = int(time.time())
                    filename = f"drowsiness_frame_{timestamp}.jpg"
                    cv2.imwrite(filename, processed_frame)
                    self.logger.info(f"Frame saved as {filename}")
                    print(f"Frame saved as {filename}")
        
        except KeyboardInterrupt:
            self.logger.info("System interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info("System shutdown complete")
        print("\nThank you for using the Driver Drowsiness Detection System!")


def main():
    """Main entry point."""
    detector = DrowsinessDetector()
    detector.run()


if __name__ == "__main__":
    main()