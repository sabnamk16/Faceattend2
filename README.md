# Face Recognition Attendance System with Django and OpenCV

A modern, AI-powered attendance management system that uses face recognition technology to automate student attendance tracking. Built with Django and OpenCV, this system provides real-time face detection and recognition for educational institutions.

## 🚀 Features

### Core Functionality
- **Real-Time Face Recognition:** Automatically identifies students using a webcam.
- **Attendance Tracking:** Records attendance with timestamps.
- **Student Management:** Create, view, update, and delete student records.
- **Department Organization:** Organizes students by departments and classes.
- **Face Registration:** Captures student faces and generates face encodings.

### Advanced Features
- **Live Video Stream:** Supports real-time face recognition with visual feedback.
- **Face Search:** Searches for students by uploading a photograph.
- **Attendance Analytics:** Displays attendance statistics and reports.
- **Confidence Scoring:** Shows a confidence percentage for face matching.
- **Timezone Configuration:** Supports configurable timezone settings.

### Technical Features
- **Responsive UI:** Built with Bootstrap 5 and custom CSS.
- **Database Management:** Uses Django ORM for database operations.
- **Image Processing:** Detects faces and generates face encodings.
- **Security:** Includes CSRF protection and input validation.
- **Error Handling:** Provides error handling and user feedback.

## 🛠️ Technology Stack

### Backend
- **Python:** Application programming language.
- **Django 4.2.7:** Web application framework.
- **SQLite:** Database used for development.
- **OpenCV 4.8.1:** Computer vision and image processing.
- **face-recognition 1.3.0:** Face detection and recognition.
- **NumPy 1.24.3:** Numerical computing.

### Frontend
- **HTML5 and CSS3:** Page structure and styling.
- **Bootstrap 5:** Responsive UI framework.
- **Bootstrap Icons:** Interface icons.
- **Inter Font:** Typography.
- **JavaScript:** Client-side interactions.

### Additional Libraries
- **Django Crispy Forms:** Form rendering and styling.
- **crispy-bootstrap5:** Bootstrap 5 integration for Django Crispy Forms.
- **Pillow:** Image processing.
- **pytz:** Timezone utilities.

## 📋 Requirements

### System Requirements
- Python 3.8 or later.
- Webcam for real-time face recognition.
- 4 GB RAM or more recommended.
- Modern web browser.

### Python Dependencies

The project dependencies are listed in `requirements.txt`:

```text
Django==4.2.7
opencv-python==4.8.1.78
face-recognition==1.3.0
numpy==1.24.3
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Faceattend2
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository's actual URL.

### 2. Navigate to the Django Project

If the application remains inside the nested project folder, run:

```bash
cd Face-Recognition-Attendance-System-with-Django-and-OpenCV-main
```

If you have moved the application files into the repository root, skip this step.

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The `face-recognition` library may require additional system dependencies, including CMake and dlib. Installation requirements vary by operating system.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

```text
http://127.0.0.1:8000/
```

The webcam and face recognition features require appropriate camera permissions and compatible hardware.

## 📁 Project Structure

```text
face_attendance_system/
├── face_attendance_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── students/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils.py
│   └── video_stream.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── students/
├── media/
│   ├── student_photos/
│   ├── search_photos/
│   └── temp/
├── static/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

*Note: This is a representative project structure. Actual files and directories may vary.*

## 🎯 Core Models

### Student
- **Personal Information:** Name, student ID, email, phone, date of birth, and address.
- **Academic Information:** Department, major, year, and class.
- **Face Data:** Student photograph, face encoding, and registration status.
- **Status:** Active or inactive.

### Department
- **Basic Information:** Department name, code, and description.
- **Relationships:** Can be associated with multiple students.

### AttendanceRecord
- **Attendance Data:** Student, date, check-in time, and check-out time.
- **Status:** Attendance status, such as present, absent, or late, where supported by the application.
- **Additional Information:** Confidence score and remarks.

### FaceSearchLog
- **Search Data:** Search photograph, matched student, and confidence score.
- **Status:** Search result, such as successful match, no match, or error.

## 🔍 Face Recognition Process

### 1. Face Registration
1. Capture a student's photograph using a webcam or upload an image.
2. Detect the face using the `face-recognition` library.
3. Generate a 128-dimensional face encoding.
4. Store the encoding for future recognition.

### 2. Real-Time Recognition
1. Capture video frames from the webcam.
2. Detect faces in the frames.
3. Generate encodings for detected faces.
4. Compare the encodings against registered student faces.
5. Mark attendance for recognized students according to the application's attendance rules.
6. Display recognition results and confidence information.

### 3. Face Search
1. Upload a photograph for searching.
2. Detect the face and generate its encoding.
3. Compare it with registered student encodings.
4. Display the best matching result when a suitable match is found.

## 🎨 User Interface

### Dashboard
- Statistics cards and summary information.
- Recent students and attendance records.
- Quick-action buttons.
- Responsive layout.

### Student Management
- Student listing and search.
- Student creation and editing forms.
- Face registration interface.
- Student profiles and attendance history.

### Attendance System
- Real-time video feed.
- Face recognition overlays.
- Automated attendance marking.
- Visual recognition status indicators.

## ⚙️ Configuration

### Application Settings
- **Timezone:** Configure the timezone in Django settings. For Nepal, use `Asia/Kathmandu`.
- **Media Files:** Configure storage for student photographs and face-search images.
- **Database:** SQLite for development; other Django-supported databases can be configured.
- **Static Files:** CSS, JavaScript, and other static assets.
- **Security:** CSRF protection and Django security settings.

### Face Recognition Parameters
- **Tolerance:** A face distance threshold of `0.6` may be used, depending on the implementation.
- **Detection Scale:** Frames may be resized to `0.25x` to improve processing performance.
- **Confidence Display:** Matching results may be displayed as percentages.
- **Attendance Logic:** The application can enforce one attendance check-in per student per day, if configured.

## 🔒 Security Considerations

- CSRF protection for forms.
- Input validation and sanitization.
- Django ORM to help protect against SQL injection.
- Django template escaping to reduce XSS risks.
- Appropriate validation and access controls for uploaded files.
- Secure handling of student photographs and biometric face encodings.

**Privacy note:** Face photographs and face encodings are sensitive personal data. Use appropriate consent, access controls, retention policies, and secure storage when handling real students' information.

## 📊 Performance Optimization

- Reduced-resolution video frames for faster face detection.
- Database indexing where appropriate.
- Efficient storage and retrieval of face encodings.
- Optimized database queries.
- Responsive templates and user interface.

Actual performance depends on the hardware, dataset size, and application configuration.

## 📈 Dashboard Statistics

The dashboard can display information such as:

- Total registered students.
- Number of students with registered faces.
- Total departments.
- Today's attendance count.
- Recent student and attendance activity.

## 🔮 Future Improvements

Potential enhancements include:
- Role-based access control for administrators and staff.
- Advanced attendance reports and data export.
- PostgreSQL support for production deployments.
- Docker-based deployment.
- Cloud hosting and automated CI/CD.
- Improved audit logging and monitoring.

## 👩‍💻 Author

**Sabnam Khatun**

GitHub: [@sabnamk16](https://github.com/sabnamk16)

## 📄 License

Add a license file if you intend to distribute this project under an open-source license.

![Dashboard](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Dashboard.png)

![Departments](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Departments.png)

![Face Search](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face%20search.png)

![Live Attendance](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Live%20Attendance.png)

![Student Management](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Student%20Management.png)

![Student Profile](https://github.com/sabnamk16/Faceattend2/blob/fe75de3fc2f624140023f3ff5c3af45c9571f1cb/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Face-Recognition-Attendance-System-with-Django-and-OpenCV-main/Student%20profile.png)

