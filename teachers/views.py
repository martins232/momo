from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher, Grade
from main . decorators import teacher
from teachers. forms import UserUpdateForm,TeacherUpdateForm, ChangeProfilePicture
from django.contrib.auth.decorators import login_required
from exam.forms import ExamForm, QuestionForm
from django.contrib import messages
from exam .models import Exam, Question
from teachers.models import Subject
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator, EmptyPage



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
    user = User.objects.get(id =pk)
    p_form = UserUpdateForm(request, instance = user,)
    t_form = TeacherUpdateForm(request, instance= user.teacher)
    
    if request.method == "POST":
        p_form = UserUpdateForm(request, request.POST, instance = user)
        t_form = TeacherUpdateForm(request, request.POST, instance= user.teacher)
        if t_form.is_valid():
            p_form.save()
            t_form.save()
            messages.success(request, "Profile updated")
            return redirect("edit-profile", pk =user.id)
        else:
            print("Nio")
            print(p_form.errors)
            print("Teacher: ",t_form.errors)       
    context = {
        "p_form": p_form,
        "t_form" : t_form,
        
    }
    # print(pic_form)
    return render(request, "teachers/edit_profile.html", context)
@login_required(login_url="login")
def editProfileImage(request, pk):
    
    teacher = Teacher.objects.get(id=pk)
    form = ChangeProfilePicture(instance=teacher)
    if request.method == "POST":
        form = ChangeProfilePicture(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("edit-profile", pk=request.user.id)
    context ={
        "form":form
    }
    return render(request, "teachers/image.html", context)

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
        else:
            messages.add_message(request, messages.ERROR, form.errors.as_ul())   
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

@login_required(login_url="login")
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
@login_required(login_url="login")
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
@login_required(login_url="login")
def viewAllQuestions(request):
    #filtering
    # filt_subject= request.GET.get("subject") if request.GET.get("subject") != None else ""
    # filt_question= request.GET.get("question") if request.GET.get("question") != None else ""
    # filt_grade= request.GET.get("grade") if request.GET.get("grade") != None else 0
    filt_subject= request.GET.get("subject", "") 
    filt_question= request.GET.get("question", "") 
    filt_grade= request.GET.get("grade", 0) 
    #########
   
    teacher = User.objects.get(username=request.user.username)
    questions = teacher.question_set.filter(
            Q(exam__subject__name__exact=filt_subject) | 
            Q(exam__grade__grade__exact=filt_grade) |
            Q(question__exact=filt_question)
            )
    
    # if filt_subject or int(filt_grade):  #for some reasons i don't know why, if i remove the int the logic becomes true 
    #     questions = teacher.question_set.filter(
    #         Q(exam__subject__name__exact=filt_subject) | 
    #         Q(exam__grade__grade__exact=filt_grade) 
    #         )

    # else:
    #     questions = teacher.question_set.filter(Q(question__contains=filt_question))
        
    
    #for drop down in search box
    subjects = teacher.subject_set.all()
    grades = Grade.objects.all()
    

    
  
    context ={
        "questions":questions,
        "subjects": subjects,
        "grades": grades
    }
    return render(request, "teachers/view_all_question.html", context)

