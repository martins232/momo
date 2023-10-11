from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher
from . forms import TeacherUpdateForm
from django.contrib.auth.decorators import login_required
from exam.forms import ExamForm, QuestionForm
from django.contrib import messages
from exam .models import Exam
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.
@login_required(login_url="login")
def userProfile(request):
    user = User.objects.get(username = request.user.username)
    subjects = user.subject_set.all()
    context = {
        "user": user,
        "subjects":subjects,
        "count_course" : len(user.subject_set.all())
    }
    return render(request, "teachers/profile.html", context)

@login_required(login_url="login")
def editProfile(request, pk):
    teacher = Teacher.objects.get(user=pk)
    # print(type(teacher))
    t_form = TeacherUpdateForm(request, instance= teacher)
    if request.method == "POST":
        t_form = TeacherUpdateForm(request,data=request.POST, files=request.FILES,  instance= teacher)
        if t_form.is_valid():
            t_form.save()
            return redirect("edit-profile", pk = teacher.user.id)
        
    context = {
        "t_form" : t_form
    }
    return render(request, "teachers/edit_profile.html", context)

@login_required(login_url="login")
def createExam(request):
    #form to create exam
    form = ExamForm(request, request.POST or None)
    
    #get all the exams by this user
    exams = User.objects.get(username=request.user.username).exam_set.all()
    
    if request.method == "POST":
        form = ExamForm(request, request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.add_message(request, messages.SUCCESS, "Exam created")
            return redirect("exam")
            
    context = {
        "form": form,
        "exams": exams,
    }
    return render(request, "teachers/exam.html", context)

@login_required(login_url="login")
def deleteExam(request, pk):
    exam = get_object_or_404(Exam, id=pk)
    if request.user != exam.teacher:
        return redirect("home")
    if request.method== "POST":
        exam = get_object_or_404(Exam, id=request.POST["obj"])
        exam.delete()
        messages.add_message(request, messages.SUCCESS, "Exam deleted")
        return redirect("exam")
    context = {
        "obj": exam,
        "obj_name":"Exam"}    
    return render(request, "teachers/delete.html", context)

@login_required(login_url="login")
def editExam(request, pk):
    exam = get_object_or_404(Exam, id=pk)
    if request.user != exam.teacher:
        return redirect("home")
    form = ExamForm(request, instance=exam) 
    if request.method == "POST":
        form = ExamForm(request, request.POST, instance=exam) 
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Exam saved")
            return redirect("exam")
        
    context = {
        "form": form
    }  
    return render(request, "teachers/edit_exam.html", context) 


def viewExam(request, pk):
    try:
        exam = Exam.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect("404")
    
    form = QuestionForm()
    context = {
        "exam": exam,
        "form": form
    }
    return render(request, "teachers/view_exam.html", context)
    
