from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
	id = models.AutoField(primary_key=True)
	address = models.TextField()
	objects = models.Manager()

class Students(models.Model):
	id = models.AutoField(primary_key=True)
	gender = models.CharField(max_length=50)
	address = models.TextField()
	objects = models.Manager()

class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=40)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

classes=[('one','one'),('two','two'),('three','three'),('four','four')]

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    cl= models.CharField(max_length=10,choices=classes,default='one')   # default
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Subjects(models.Model):
	id =models.AutoField(primary_key=True)
	subject_name = models.CharField(max_length=255)
	teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
	objects = models.Manager()

class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)

class AttendanceReport(models.Model):	
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
	attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
	objects = models.Manager()

class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True)
    message=models.CharField(max_length=500)

class StudentResult(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
	subject_exam_marks = models.FloatField(default=0)
	objects = models.Manager()

class Document(models.Model):    
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)