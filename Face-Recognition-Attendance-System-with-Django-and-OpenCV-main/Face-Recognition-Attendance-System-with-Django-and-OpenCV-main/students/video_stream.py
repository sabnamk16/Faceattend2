import cv2
import face_recognition
import numpy as np
import pickle
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from .models import Student, AttendanceRecord
import pytz

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.load_known_faces()
        # Get China timezone
        self.china_tz = pytz.timezone(settings.TIME_ZONE)
    
    def load_known_faces(self):
        """Load all registered student face encodings"""
        students = Student.objects.filter(is_face_registered=True)
        self.known_encodings = []
        self.known_students = []
        
        for student in students:
            if student.face_encoding:
                try:
                    encoding = pickle.loads(student.face_encoding)
                    self.known_encodings.append(encoding)
                    self.known_students.append(student)
                except Exception as e:
                    print(f"Error loading encoding for {student.student_id}: {e}")
        
        print(f"Loaded {len(self.known_encodings)} face encodings")
    
    def __del__(self):
        self.video.release()
    
    def mark_attendance(self, student, confidence):
        """
        Mark attendance with China timezone
        """
        # Get current time in China timezone
        now_china = timezone.now().astimezone(self.china_tz)
        today = now_china.date()
        current_time = now_china.time()
        
        # Check if attendance already exists for today
        attendance, created = AttendanceRecord.objects.get_or_create(
            student=student,
            date=today,
            defaults={
                'time_in': current_time,
                'status': 'present',
                'confidence_score': confidence
            }
        )
        
        if created:
            print(f"✓ Check-in: {student.name} at {current_time} (China Time)")
            return attendance, True
        else:
            # Already checked in today
            return attendance, False
    
    def get_frame(self):
        """Process frame and return JPEG bytes"""
        success, frame = self.video.read()
        if not success:
            return None
        
        # Get frame dimensions for dynamic text sizing
        height, width = frame.shape[:2]
        font_scale = min(width, height) / 800
        thickness = max(3, int(min(width, height) / 250))
        
        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            name = "Unknown"
            confidence = 0
            student_obj = None
            status_text = ""
            
            if len(self.known_encodings) > 0:
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        student = self.known_students[best_match_index]
                        student_obj = student
                        name = student.name
                        confidence = (1 - face_distances[best_match_index]) * 100
                        
                        # Mark attendance with China timezone
                        attendance, is_new = self.mark_attendance(student, confidence)
                        
                        # Set status text for display
                        if is_new:
                            status_text = "CHECKED IN"
                        else:
                            status_text = "PRESENT"
            
            # Draw rectangle and text
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)
            
            # Calculate text dimensions
            display_text = name
            (text_width, text_height), baseline = cv2.getTextSize(
                display_text, 
                cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, 
                thickness
            )
            
            # Draw name background and text
            cv2.rectangle(
                frame, 
                (left, bottom - text_height - baseline - 20), 
                (right, bottom), 
                color, 
                cv2.FILLED
            )
            
            cv2.putText(
                frame, 
                display_text, 
                (left + 6, bottom - 10), 
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, 
                (255, 255, 255), 
                thickness,
                cv2.LINE_AA
            )
            
            # Add status badge (CHECKED IN / PRESENT)
            if status_text and student_obj:
                (status_width, status_height), status_baseline = cv2.getTextSize(
                    status_text, 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    font_scale * 0.6, 
                    max(1, thickness - 1)
                )
                
                badge_x = left
                badge_y = top - 15
                
                # Green for checked in, light green for present
                badge_color = (0, 255, 0) if status_text == "CHECKED IN" else (0, 200, 0)
                
                cv2.rectangle(
                    frame,
                    (badge_x, badge_y - status_height - 10),
                    (badge_x + status_width + 10, badge_y),
                    badge_color,
                    cv2.FILLED
                )
                
                cv2.putText(
                    frame,
                    status_text,
                    (badge_x + 5, badge_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale * 0.6,
                    (255, 255, 255),
                    max(1, thickness - 1),
                    cv2.LINE_AA
                )
            
            # Add confidence badge
            if confidence > 0:
                conf_text = f"{confidence:.1f}%"
                (conf_width, conf_height), conf_baseline = cv2.getTextSize(
                    conf_text, 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    font_scale * 0.7, 
                    max(1, thickness - 1)
                )
                
                badge_x = right - conf_width - 10
                badge_y = top - 10
                
                cv2.rectangle(
                    frame,
                    (badge_x - 5, badge_y - conf_height - 5),
                    (badge_x + conf_width + 5, badge_y + 5),
                    (0, 200, 0),
                    cv2.FILLED
                )
                
                cv2.putText(
                    frame,
                    conf_text,
                    (badge_x, badge_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale * 0.7,
                    (255, 255, 255),
                    max(1, thickness - 1),
                    cv2.LINE_AA
                )
        
        # Show current China time in video feed
        now_china = timezone.now().astimezone(self.china_tz)
        today_count = AttendanceRecord.objects.filter(date=now_china.date()).count()
        status_text = f"Time: {now_china.strftime('%H:%M:%S')} | Today: {today_count}"
        
        cv2.putText(
            frame,
            status_text,
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale * 0.8,
            (0, 255, 0),
            thickness,
            cv2.LINE_AA
        )
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes() if ret else None

def generate_frames():
    """Generator for video streaming"""
    camera = VideoCamera()
    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        del camera
