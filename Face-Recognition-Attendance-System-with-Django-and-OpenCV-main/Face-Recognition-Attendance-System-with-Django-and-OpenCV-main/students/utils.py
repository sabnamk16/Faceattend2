import face_recognition
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import pickle

def encode_face(image_path):
    """
    Generate face encoding from image path
    """
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) > 0:
            # Return the first face encoding as pickled bytes
            return pickle.dumps(face_encodings[0])
        return None
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None

def encode_face_from_array(image_array):
    """
    Generate face encoding from numpy array
    """
    try:
        rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image)
        
        if len(face_encodings) > 0:
            return pickle.dumps(face_encodings[0])
        return None
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None

def compare_faces(known_encoding_bytes, unknown_image_path, tolerance=0.6):
    """
    Compare known face encoding with unknown face image
    Returns (match, distance)
    """
    try:
        # Load known encoding
        known_encoding = pickle.loads(known_encoding_bytes)
        
        # Load and encode unknown image
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        
        if len(unknown_encodings) == 0:
            return False, None
        
        unknown_encoding = unknown_encodings[0]
        
        # Compare faces
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=tolerance)
        face_distance = face_recognition.face_distance([known_encoding], unknown_encoding)
        
        return matches[0], float(face_distance[0])
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return False, None

def find_matching_student(unknown_image_path, students_queryset):
    """
    Find matching student from database
    Returns (student, confidence_score)
    """
    try:
        # Load unknown image
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        
        if len(unknown_encodings) == 0:
            return None, None
        
        unknown_encoding = unknown_encodings[0]
        
        # Get all registered students
        registered_students = students_queryset.filter(is_face_registered=True)
        
        best_match = None
        best_distance = float('inf')
        
        for student in registered_students:
            if student.face_encoding:
                known_encoding = pickle.loads(student.face_encoding)
                face_distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
                
                if face_distance < best_distance and face_distance < 0.6:
                    best_distance = face_distance
                    best_match = student
        
        if best_match:
            confidence = (1 - best_distance) * 100
            return best_match, confidence
        
        return None, None
    except Exception as e:
        print(f"Error finding matching student: {e}")
        return None, None

def detect_faces_in_frame(frame):
    """
    Detect faces in video frame
    Returns list of face locations
    """
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    
    # Scale back up face locations
    face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
    
    return face_locations
