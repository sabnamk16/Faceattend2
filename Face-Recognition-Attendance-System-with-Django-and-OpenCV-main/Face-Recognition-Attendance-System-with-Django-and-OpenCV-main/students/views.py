from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
import base64
from PIL import Image
from io import BytesIO
import os

from .models import Student, Department, AttendanceRecord, FaceSearchLog
from .forms import StudentForm, DepartmentForm, SearchFaceForm, AttendanceFilterForm
from .utils import encode_face, find_matching_student, encode_face_from_array, compare_faces
from .video_stream import generate_frames  # Import from video_stream


# Dashboard
def dashboard(request):
    total_students = Student.objects.filter(is_active=True).count()
    registered_faces = Student.objects.filter(is_face_registered=True).count()
    total_departments = Department.objects.count()
    today_attendance = AttendanceRecord.objects.filter(date=timezone.now().date()).count()
    
    recent_students = Student.objects.filter(is_active=True).order_by('-created_at')[:5]
    recent_attendance = AttendanceRecord.objects.select_related('student').order_by('-created_at')[:10]
    
    context = {
        'total_students': total_students,
        'registered_faces': registered_faces,
        'total_departments': total_departments,
        'today_attendance': today_attendance,
        'recent_students': recent_students,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'dashboard.html', context)


# Student Management
def student_list(request):
    students = Student.objects.select_related('department').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(student_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    context = {
        'students': students,
        'search_query': search_query,
    }
    return render(request, 'students/student_list.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            
            # Generate face encoding if photo is uploaded
            if student.photo:
                encoding = encode_face(student.photo.path)
                if encoding:
                    student.face_encoding = encoding
                    student.is_face_registered = True
                    student.save()
                    messages.success(request, f'Student {student.name} created and face registered successfully!')
                else:
                    messages.warning(request, f'Student created but face registration failed. Please capture face separately.')
            else:
                messages.success(request, f'Student {student.name} created successfully!')
            
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Create'})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            
            # Re-generate face encoding if new photo is uploaded
            if 'photo' in request.FILES:
                encoding = encode_face(student.photo.path)
                if encoding:
                    student.face_encoding = encoding
                    student.is_face_registered = True
                    student.save()
                    messages.success(request, f'Student {student.name} updated and face re-registered!')
                else:
                    messages.warning(request, f'Student updated but face registration failed.')
            else:
                messages.success(request, f'Student {student.name} updated successfully!')
            
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Update', 'student': student})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendance_records = student.attendances.all()[:20]
    
    # Attendance statistics
    total_attendance = student.attendances.count()
    present_count = student.attendances.filter(status='present').count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total_attendance': total_attendance,
        'present_count': present_count,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    return render(request, 'students/student_detail.html', context)


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'Student {student.name} deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})


# Face Capture
def capture_face(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/capture_face.html', {'student': student})


@csrf_exempt
def save_face_encoding(request, student_id):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, student_id=student_id)
            
            # Get image data from request
            data = json.loads(request.body)
            image_data = data.get('image')
            
            # Decode base64 image
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Save image
            os.makedirs('media/student_photos', exist_ok=True)
            image_path = f'media/student_photos/{student.student_id}_face.jpg'
            image.save(image_path)
            
            # Generate encoding
            encoding = encode_face(image_path)
            
            if encoding:
                student.face_encoding = encoding
                student.is_face_registered = True
                student.save()
                
                return JsonResponse({'success': True, 'message': 'Face registered successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'No face detected in image'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# Face Search
def search_face(request):
    result = None
    
    if request.method == 'POST':
        form = SearchFaceForm(request.POST, request.FILES)
        if form.is_valid():
            photo = request.FILES['photo']
            
            # Save temporary file
            os.makedirs('media/temp', exist_ok=True)
            temp_path = f'media/temp/temp_search_{datetime.now().timestamp()}.jpg'
            with open(temp_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
            
            # Find matching student
            student, confidence = find_matching_student(temp_path, Student.objects.all())
            
            # Log the search
            log = FaceSearchLog.objects.create(
                search_photo=photo,
                matched_student=student,
                confidence_score=confidence,
                search_status='success' if student else 'no_match'
            )
            
            if student:
                result = {
                    'found': True,
                    'student': student,
                    'confidence': round(confidence, 2)
                }
                messages.success(request, f'Match found: {student.name} with {round(confidence, 2)}% confidence')
            else:
                result = {'found': False}
                messages.warning(request, 'No matching student found in database')
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        form = SearchFaceForm()
    
    return render(request, 'students/search_face.html', {'form': form, 'result': result})


# Real-time Attendance
def realtime_attendance(request):
    return render(request, 'students/realtime_attendance.html')


def video_feed(request):
    """
    Video streaming route - uses generate_frames from video_stream.py
    """
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


# Attendance Records
def attendance_list(request):
    records = AttendanceRecord.objects.select_related('student').all()
    
    form = AttendanceFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['student']:
            records = records.filter(student=form.cleaned_data['student'])
        if form.cleaned_data['date_from']:
            records = records.filter(date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            records = records.filter(date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data['status']:
            records = records.filter(status=form.cleaned_data['status'])
    
    context = {
        'records': records,
        'form': form,
    }
    return render(request, 'students/attendance_record.html', context)


# Department Management
def department_list(request):
    departments = Department.objects.annotate(student_count=Count('students'))
    return render(request, 'students/department_list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'students/department_form.html', {'form': form, 'action': 'Create'})


def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department {department.name} updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'students/department_form.html', {
        'form': form, 
        'action': 'Update',
        'department': department
    })


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f'Department {department_name} deleted successfully!')
        return redirect('department_list')
    
    return render(request, 'students/department_confirm_delete.html', {'department': department})
