from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher
from main . decorators import teacher
from . forms import TeacherUpdateForm
from django.contrib.auth.decorators import login_required
from exam.forms import ExamForm, QuestionForm
from django.contrib import messages
from exam .models import Exam, Question
from teachers.models import Subject
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.signals import post_save
from django.dispatch import receiver




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

@receiver(post_save, sender=Subject)
def set_exam_teacher_null(sender, instance, **kwargs):
    """
    This function is used to transfer subsject, exams and question from one teacher to another
    """
    # instance is the subject object that was deleted
    # get the exams that are related to this subject
    exams = Exam.objects.filter(subject=instance)
    # # # loop through the exams and set their teacher to null
    for exam in exams:
        exam.teacher = instance.teacher
        questions =exam.question_set.filter(exam=exam)
        exam.save()
        for question in questions:
            question.teacher = instance.teacher
            question.save()
        

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
        "form": form,
        "obj_name": "EXAM"
    }  
    return render(request, "teachers/edit.html", context) 


def viewExam(request, pk):
    try:
        exam = Exam.objects.get(id=pk)
        questions= exam.question_set.all()
    except ObjectDoesNotExist:
        return redirect("404")
    
    form = QuestionForm(request.POST or None)
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
           question = form.save(commit=False)
           question.teacher = request.user
           question.exam = exam
           question.save()
           return redirect("view-exam", pk=exam.id)
        
    
    context = {
        "exam": exam,
        "form": form,
        "questions":questions
    }
    return render(request, "teachers/view_exam.html", context)

def editQuestion(request, pk):
    try:
        question= Question.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect("404")
    
    form = QuestionForm(instance=question)
    
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) 
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Exam saved")
            return redirect("view-exam", pk = question.exam.id)
        
    context = {
        "form": form,
        "obj_name": "QUESTION"
    }  
    return render(request, "teachers/edit.html", context) 
    
    
    
@login_required(login_url="login")
def deleteQuestion(request, pk):
    question = get_object_or_404(Question, id=pk)
    if request.user != question.exam.teacher:
        return redirect("404")
    if request.method== "POST":
        exam = get_object_or_404(Question, id=pk)
        exam.delete()
        messages.add_message(request, messages.SUCCESS, "Question deleted")
        return redirect("exam")
    context = {
        "obj": question,
        "obj_name":"Question"}    
    return render(request, "teachers/delete.html", context)

@teacher
def viewAllQuestions(request):
    teacher = User.objects.get(username=request.user.username)
    questions = teacher.question_set.all()
    context ={
        "questions":questions
    }
    return render(request, "teachers/view_all_question.html", context)