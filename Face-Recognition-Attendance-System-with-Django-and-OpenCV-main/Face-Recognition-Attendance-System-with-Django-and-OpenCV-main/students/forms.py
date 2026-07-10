from django import forms
from .models import Student, Department, AttendanceRecord
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'phone', 'department', 
                  'major', 'year', 'class_name', 'date_of_birth', 'address', 
                  'photo', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Column('student_id', css_class='col-md-6'),
                    Column('name', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Column('email', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Column('department', css_class='col-md-6'),
                    Column('major', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Column('year', css_class='col-md-6'),
                    Column('class_name', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Column('date_of_birth', css_class='col-md-6'),
                    Column('is_active', css_class='col-md-6'),
                    css_class='row'
                ),
                'address',
                'photo',
                css_class='needs-validation'
            )
        )

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SearchFaceForm(forms.Form):
    photo = forms.ImageField(label='Upload Photo to Search')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Search', css_class='btn btn-primary'))

class AttendanceFilterForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(is_active=True),
        required=False,
        label='Student'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From Date'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To Date'
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + AttendanceRecord._meta.get_field('status').choices,
        required=False
    )
