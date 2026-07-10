from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Student, Department, AttendanceRecord, FaceSearchLog

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'student_count', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']
    ordering = ['code']
    
    def student_count(self, obj):
        count = obj.students.count()
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    student_count.short_description = 'Total Students'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'email', 'department', 'year', 
                    'face_status', 'status_badge', 'created_at']
    list_filter = ['is_active', 'is_face_registered', 'department', 'year', 'created_at']
    search_fields = ['student_id', 'name', 'email', 'phone']
    readonly_fields = ['face_encoding', 'created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'name', 'email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('department', 'major', 'year', 'class_name')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'address')
        }),
        ('Face Recognition', {
            'fields': ('photo', 'is_face_registered', 'face_encoding'),
            'classes': ('collapse',)
        }),
        ('Status & Timestamps', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def face_status(self, obj):
        if obj.is_face_registered:
            return format_html('<span style="color: green;">✓ Registered</span>')
        return format_html('<span style="color: orange;">⚠ Pending</span>')
    face_status.short_description = 'Face Status'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; '
            'padding: 3px 10px; border-radius: 3px;">Inactive</span>'
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} students marked as active.')
    mark_as_active.short_description = 'Mark selected students as active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} students marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected students as inactive'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    # Remove 'time_out' from list_display
    list_display = ['student_info', 'date', 'time_in', 
                    'status_badge', 'confidence_display', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['student__student_id', 'student__name']
    date_hierarchy = 'date'
    list_per_page = 50
    ordering = ['-date', '-time_in']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Attendance Details', {
            # Remove 'time_out' from here or make it read-only
            'fields': ('date', 'time_in', 'status')
        }),
        ('Additional Information', {
            'fields': ('confidence_score', 'remarks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.student.name,
            obj.student.student_id
        )
    student_info.short_description = 'Student'
    
    def status_badge(self, obj):
        colors = {
            'present': '#28a745',
            'absent': '#dc3545',
            'late': '#ffc107'
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def confidence_display(self, obj):
        if obj.confidence_score is not None:
            try:
                conf_value = float(obj.confidence_score)
                color = '#28a745' if conf_value > 80 else '#ffc107'
                html = '<span style="color: %s; font-weight: bold;">%.2f%%</span>' % (color, conf_value)
                return mark_safe(html)
            except (ValueError, TypeError):
                return '-'
        return '-'
    confidence_display.short_description = 'Confidence'

@admin.register(FaceSearchLog)
class FaceSearchLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'matched_student_info', 'search_status_badge', 
                    'confidence_display', 'created_at']
    list_filter = ['search_status', 'created_at']
    search_fields = ['matched_student__name', 'matched_student__student_id']
    readonly_fields = ['search_photo', 'matched_student', 'confidence_score', 
                       'search_status', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_per_page = 30
    ordering = ['-created_at']
    
    def matched_student_info(self, obj):
        if obj.matched_student:
            return format_html(
                '<strong>{}</strong><br><small>{}</small>',
                obj.matched_student.name,
                obj.matched_student.student_id
            )
        return format_html('<span style="color: #6c757d;">No Match</span>')
    matched_student_info.short_description = 'Matched Student'
    
    def search_status_badge(self, obj):
        colors = {
            'success': '#28a745',
            'no_match': '#ffc107',
            'error': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.search_status, '#6c757d'),
            obj.get_search_status_display()
        )
    search_status_badge.short_description = 'Status'
    
    def confidence_display(self, obj):
        if obj.confidence_score is not None:
            # Convert to Python float explicitly
            try:
                conf_value = float(obj.confidence_score)
                # Use % operator instead of .format()
                html = '<span style="font-weight: bold;">%.2f%%</span>' % conf_value
                return mark_safe(html)
            except (ValueError, TypeError):
                return '-'
        return '-'
    confidence_display.short_description = 'Confidence'

# Customize Admin Site Header
admin.site.site_header = "Face Recognition Attendance System"
admin.site.site_title = "FaceAttend Admin"
admin.site.index_title = "Welcome to FaceAttend Administration"
