from django.db import models
from django.core.validators import RegexValidator
import os

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Department(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']

class Student(BaseModel):
    # Basic Information
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'Only uppercase letters and numbers allowed')]
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number')]
    )
    
    # Academic Information
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    major = models.CharField(max_length=100)
    year = models.IntegerField(choices=[(1, 'First Year'), (2, 'Second Year'), 
                                         (3, 'Third Year'), (4, 'Fourth Year')])
    class_name = models.CharField(max_length=50)
    
    # Personal Information
    date_of_birth = models.DateField()
    address = models.TextField()
    
    # Face Recognition Data
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)
    is_face_registered = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.name}"
    
    class Meta:
        ordering = ['student_id']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['name']),
        ]

class AttendanceRecord(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late'),
        ],
        default='present'
    )
    confidence_score = models.FloatField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.student_id} - {self.date} - {self.status}"
    
    class Meta:
        ordering = ['-date', '-time_in']
        unique_together = ['student', 'date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['student', 'date']),
        ]

class FaceSearchLog(BaseModel):
    search_photo = models.ImageField(upload_to='search_photos/')
    matched_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    search_status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('no_match', 'No Match'),
            ('error', 'Error'),
        ]
    )
    
    def __str__(self):
        return f"Search {self.id} - {self.search_status}"
    
    class Meta:
        ordering = ['-created_at']
