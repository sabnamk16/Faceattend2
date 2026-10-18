Face Recognition Attendance System with Django and OpenCV.
A modern, AI-powered attendance management system that uses face recognition technology to automate student attendance tracking. Built with Django and OpenCV, this system provides real-time face detection and recognition capabilities for educational institutions.

🚀 Features
Core Functionality
-Real-time Face Recognition: Automatic student identification using webcam
-Attendance Tracking: Automated check-in/check-out with timestamp recording
-Student Management: Complete CRUD operations for student records
-Department Organization: Organize students by departments and classes
-Face Registration: Easy face capture and encoding for new students

Advanced Features
-Live Video Stream: Real-time attendance marking with visual feedback
-Face Search: Search students by uploading their photo
-Attendance Analytics: View attendance statistics and reports
-Confidence Scoring: Face matching with confidence percentage
-Timezone Support: Configured for China Standard Time (CST)

Technical Features
-Modern UI: Responsive design with Bootstrap 5 and custom gradients
-Database Optimization: Efficient queries with proper indexing
-Image Processing: Automatic face detection and encoding
-Security: CSRF protection and secure file uploads
-Error Handling: Comprehensive error management and user feedback

🛠️ Technology Stack

Backend
Django 4.2.7: Python web framework
SQLite: Database (development)
face-recognition 1.3.0: Face recognition library
OpenCV 4.8.1: Computer vision and image processing
NumPy 1.24.3: Numerical computing

Frontend
Bootstrap 5: Modern CSS framework
Bootstrap Icons: Icon library
Inter Font: Modern typography
Custom CSS: Gradient backgrounds and animations
Development Tools
Django Crispy Forms: Form styling with Bootstrap 5
Pillow 10.1.0: Image processing
pytz: Timezone handling

📋 Requirements

System Requirements
Python 3.8+
Webcam (for face recognition)
4GB+ RAM recommended
Modern web browser
Python Dependencies
Django==4.2.7
opencv-python==4.8.1.78
face-recognition==1.3.0
numpy==1.24.3
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7


📁 Project Structure
face_attendance_system/
├── face_attendance_system/     # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── students/                  # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Django forms
│   ├── utils.py              # Utility functions
│   └── video_stream.py       # Face recognition logic
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── dashboard.html        # Dashboard view
│   └── students/             # Student-specific templates
├── media/                    # Uploaded files
│   ├── student_photos/       # Student face photos
│   ├── search_photos/        # Search query photos
│   └── temp/                 # Temporary files
├── static/                   # Static files (CSS, JS)
├── db.sqlite3               # SQLite database
├── manage.py               # Django management
└── requirements.txt        # Python dependencies

🎯 Core Models

Student Model
Personal Info: Name, ID, email, phone, date of birth, address
Academic Info: Department, major, year, class
Face Data: Photo, face encoding, registration status
Status: Active/inactive flag

Department Model
Basic Info: Name, code, description
Relationships: One-to-many with students

AttendanceRecord Model
Attendance Data: Student, date, time-in, time-out
Status: Present, absent, late
Metadata: Confidence score, remarks

FaceSearchLog Model
Search Data: Search photo, matched student, confidence
Status: Success, no match, error

🔍 Face Recognition Process

1. Face Registration
Student photo is captured via webcam or uploaded
Face detection using face_recognition library
Face encoding generation (128-dimensional vector)
Encoding stored in database as binary data

2. Real-time Recognition
Webcam captures video frames
Face detection in each frame
Face encoding generation for detected faces
Comparison with known student encodings
Attendance marking for recognized students
Visual feedback with name and confidence score

3. Face Search
Upload photo for search
Face detection and encoding
Comparison with all registered students
Return best match with confidence score

🎨 User Interface
Dashboard
Statistics cards with gradient backgrounds
Recent students and attendance records
Quick action buttons
Responsive design for all devices
Student Management
Student list with search functionality
Create/edit forms with validation
Face capture interface
Detailed student profiles with attendance history
Attendance System
Real-time video feed
Live face recognition overlay
Automatic attendance marking
Visual status indicators

⚙️ Configurations
Settings Highlights
Timezone: Asia/Kathmandu
Media Files: Student photos and search images
Database: SQLite (easily configurable for PostgreSQL/MySQL)
Static Files: Bootstrap 5 CDN integration
Security: CSRF protection enabled
Face Recognition Parameters
Tolerance: 0.6 (60% similarity threshold)
Detection Scale: 0.25x for performance
Confidence Display: Percentage-based scoring
Attendance Logic: One check-in per day per student

🔒 Security Considerations
CSRF protection for all forms
Secure file upload handling
Input validation and sanitization
SQL injection prevention (Django ORM)
XSS protection (Django templates)

🚀 Performance Optimization
Face detection at reduced resolution (0.25x)
Database indexing on frequently queried fields
Efficient face encoding storage (binary format)
Lazy loading of student data
Optimized template rendering

📊 Usage Statistics
The dashboard provides real-time statistics:

-Total registered students
-Number of faces registered
-Department count
-Today's attendance count
-Recent activity feeds

![Dashboard](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Dashboard.png)

![Departments](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Departments.png)

![Face Search](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face%20search.png)

![Live Attendance](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Live%20Attendance.png)

![Student Management](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Student%20Management.png)

![Student Profile](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Student%20profile.png)

