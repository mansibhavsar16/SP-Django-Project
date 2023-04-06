from django.shortcuts import render,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import DocumentForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Document

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')


#for showing login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacherclick.html')

#for showing login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'studentclick.html')

#signup for student
def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'studentsignup.html',context=mydict)


#for checking user is techer , student 
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('teacher-dashboard')
        else : 
            return render(request,'teacherclick.html')
            # return redirect('teacherlogin')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('student-dashboard')
        else : 
            return redirect('studentlogin')


# for TEACHER 
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(user_id=request.user.id)
    studentcount=models.StudentExtra.objects.all().filter().count()
    notice=models.Notice.objects.all()
    mydict={
        'studentcount':studentcount,
        'notice': notice
    }
    return render(request,'teacher_dashboard.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_view(request):
    students=models.StudentExtra.objects.all().order_by('roll').filter()
    return render(request,'teacher_view_student.html',{'students':students})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'teacher_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'teacher_notice.html',{'form':form})


#FOR STUDENT AFTER THEIR Login
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        # 'roll':studentdata[0].roll,
        # 'mobile':studentdata[0].mobile,
        'notice':notice
    }
    return render(request,'student_dashboard.html',context=mydict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'student_view_attendance_ask_date.html',{'form':form})

def student_marks_view(request) :
    return render(request,'marksgraph.html')

# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher)
class DocumentCreateView(CreateView):    
    model = Document
    form_class = DocumentForm
    template_name = 'teacher_upload_document.html'
    success_url = reverse_lazy('teacher-dashboard')        
  
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
def download(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
    return response

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
class DocumentListView(ListView):
    model = Document
    template_name = 'student_view_document.html'
    context_object_name = 'documents'
    
    
def give_marks(request,pk):
    marks_given = False
    student = get_object_or_404(models.Student,pk = pk)
    form = forms.MarksForm(request.POST)
    if form.is_valid():
        marks = form.save(commit=False)
        marks.student = student
        marks.save()
        return redirect('give-marks')
    else:
        form = forms.MarksForm()
    return render(request,'give_marks.html',{'form':form,'student':student,'marks_given' : marks_given})
    