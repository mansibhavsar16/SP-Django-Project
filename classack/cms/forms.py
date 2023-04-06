from django import forms
from django.contrib.auth.models import User
from . import models

#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile']


#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['mobile']


#for Attendance related form
presence_choices=('Present','Present'),('Absent','Absent')
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()

#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'

#for study material related form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ('description', 'document')
        
class MarksForm(forms.ModelForm):
    class Meta():
        model = models. StudentResult()
        fields  = ['subject_id','subject_exam_marks']