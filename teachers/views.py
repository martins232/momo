
import json
from operator import le
from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher, Grade
from main . decorators import teacher
from teachers. forms import UserUpdateForm,TeacherUpdateForm, ChangeProfilePicture
from django.contrib.auth.decorators import login_required
from exam.forms import ExamForm, QuestionForm
from django.contrib import messages
from exam .models import Exam, Question, Session
from teachers.models import Subject
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator, EmptyPage
from django.http.response import JsonResponse
from django.db.models import Count, Avg




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
@teacher
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
           messages.add_message(request, messages.ERROR, p_form.errors.as_ul())      
           messages.add_message(request, messages.ERROR, t_form.errors.as_ul())      
    context = {
        "p_form": p_form,
        "t_form" : t_form,
        
    }
    return render(request, "teachers/edit_profile.html", context)
@teacher
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
@teacher
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
@teacher
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
        
@teacher
@login_required(login_url="login")
def deleteExam(request, pk):
    exam = get_object_or_404(Exam, id=pk)
    if request.user != exam.teacher:
        return redirect("404")
    exam.delete()
    messages.add_message(request, messages.SUCCESS, "Exam deleted")
    return redirect("exam")
    
@teacher
@login_required(login_url="login")
def editExam(request, pk):
    exam = get_object_or_404(Exam, id=pk)
    if request.user != exam.teacher:
        return redirect("404")
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


@teacher
@login_required(login_url="login")
def viewExam(request, pk):
    try:
        exam = Exam.objects.get(id=pk)
        questions= exam.question_set.all()
    except ObjectDoesNotExist:
        return redirect("404")
    
    if request.user != exam.teacher:
        return redirect("404")
    
    
    form = QuestionForm(request, request.POST or None)
    
    if request.method == "POST":
        form = QuestionForm(request, request.POST)
        if form.is_valid():
           question = form.save(commit=False)
           question.subject = exam.subject
           question.exam = exam
           question.save()
           return redirect("view-exam", pk=exam.id)
        else:
            print(form.errors)
        
        
    
    context = {
        "exam": exam,
        "form": form,
        "questions":questions
    }
    return render(request, "teachers/view_exam.html", context)
# @teacher
# @login_required(login_url="login")
# def editQuestion(request, pk):
#     try:
#         question= Question.objects.get(id=pk)
#     except ObjectDoesNotExist:
#         return redirect("404")
    
#     form = QuestionForm(instance=question)
    
#     if request.method == "POST":
#         form = QuestionForm(request.POST, instance=question) 
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, "Exam saved")
#             # return redirect(request.META.get('HTTP_REFERER', '/'))
#             return redirect("view-exam", pk = question.exam.id)
        
#     context = {
#         "form": form,
#         "obj_name": "QUESTION"
#     }  
#     return render(request, "teachers/edit.html", context) 
    

@teacher 
@login_required(login_url="login")
def deleteQuestion(request, pk):
    question = get_object_or_404(Question, id=pk)
    if request.user != question.exam.teacher:
        return redirect("404")
    
    exam = get_object_or_404(Question, id=pk)
    exam.delete()
    messages.add_message(request, messages.SUCCESS, "Question deleted")
    return redirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect("all-questions")
      
    

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


def sessionDashboardData(request, pk):
    exam = get_object_or_404(Exam, id=pk)
    students = User.objects.filter(is_student=True, student__grade=exam.grade, student__status="Approved").exclude(id__in=Session.objects.filter(exam=exam).values("user"))
    sessions = list(Session.objects.filter(exam=exam).values("user", "score", "elapsed_time", "completed", "misconduct", "time_started"))
    data = []
    for session in sessions:
        session["name"] = User.objects.get(id=session["user"]).get_full_name()
        data.append(session)

    for student in students:
        session = {
            "user": student.id,
            "score": None,
            "elapsed_time": None,
            "completed": None,
            "misconduct": None,
            "time_started": None,
            "name": student.get_full_name(),
        }
        data.append(session)   
    return JsonResponse({"pass_mark":exam.pass_mark, "rows": data})
    
####################################################################
def sessionDashboard(request, pk):
    exam = Exam.objects.get(id=pk)
    
    questions = Question.objects.filter(exam=exam)
    total_student = exam.grade.student_set.filter(status="Approved").count()
    misconduct = Session.objects.filter(exam = exam, misconduct=True).count()
    completed = Session.objects.filter(exam = exam, completed=True).count()
    passed = Session.objects.filter(exam = exam,score__gte=exam.pass_mark, completed=True).count()
    
    try:
        avg_score = Session.objects.filter(exam=exam, completed=True).aggregate(score=Avg("score"))["score"]
        avg_score = round(avg_score, 1)
    except Exception as e:
        avg_score = "-"
    # dict(Session.objects.filter(exam=1).values_list("misconduct").annotate(count=Count("misconduct", distinct=True)))
    
    context ={
        "exam": exam,
        "exam_id": exam.id,
        "avg_score": avg_score,
        "questions": questions,
        "total_student": total_student,
        "misconduct": misconduct,
        "completed": completed,
        "passed": passed,
        "fail" : completed - passed,
        
    }
    return render(request, "teachers/session_dashboard.html", context)

def studentPerformance(request, pk):
    student_name = request.GET.get("student")
    id = request.GET.get("id")
    
    exam = Exam.objects.get(id=pk)
    student = User.objects.get(id=id)
    session = Session.objects.get(exam=exam, user=student)
    choices = session.choices
    
    questions = exam.question_set.all().values()
            
    data_ =[]
    
    
    no_correct = 0
    no_incorrect = 0
    no_unanswered = 0
    

    for question in questions:
        options = [ question["option_A"], question["option_B"], question["option_C"], question["option_D"] ]
        zipper =dict(list( zip(['A', 'B', 'C', 'D'], options)))
        answer_Abbrv =  question["answer"] # the answer in the database e.g "C"
        
        if choices[question["question"]][0] == "":
            no_unanswered += 1
        if choices[question["question"]][0] == zipper[answer_Abbrv]:
            no_correct += 1
        if choices[question["question"]][0] != zipper[answer_Abbrv]:
            no_incorrect += 1
        
        data_.append({"question": question["question"], 
                      "options_A" : question["option_A"], 
                      "options_B" : question["option_B"], 
                      "options_C" : question["option_C"], 
                      "options_D" : question["option_D"], 
                      "answer": zipper[answer_Abbrv], 
                      "choice": choices[question["question"]][0]})
        
    context = {
        "student": student,
        "exam": exam,
        "student_name": student_name,
        "session" : session,
        "data_": data_,
        "no_unanswered": no_unanswered,
        "no_correct": no_correct,
        "no_incorrect": no_incorrect
  
    }
    return render(request, "teachers/student_performance.html", context)

#JSON data after exams has been taken
def examDashboardData(request, pk):
    exam = Exam.objects.get(id = pk)
    sessions = Session.objects.filter(exam= exam)
    questions = Question.objects.filter(exam =exam)
    
    data = []
    for question in questions:
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        
        correct_student = {}
        incorrect_student = {}
        unanswered_student = {}
        
        options = {"A" :question.option_A, "B" :question.option_B, "C" :question.option_C, "D" :question.option_D,}
        
        for session in sessions:
            if session.choices[question.question][0] == "":
                unanswered_count += 1
                unanswered_student[str(session.user.id)] = str(session.user.get_full_name())
            elif session.choices[question.question][0] == options[question.answer]:
                correct_count +=1
                correct_student[str(session.user.id)] = str(session.user.get_full_name())
            elif session.choices[question.question][0] != options[question.answer]:
                incorrect_count +=1
                incorrect_student[str(session.user.id)] = session.user.get_full_name()
            
        data.append({
            "question": question.question, 
            "correct": correct_count, 
            "incorrect": incorrect_count, 
            "unanswered": unanswered_count,
            "correct_student": correct_student,
            "incorrect_student": incorrect_student,
            "unanswered_student": unanswered_student
            })
      
            
    
    
    return JsonResponse({"rows":data})
  
    
#dashboard after exams has been taken  
def examDashboard(request, pk):
    
    
    context = {"pk": pk}    
    return render(request, "teachers/exam_dashboard.html", context)


def questionData(request):
    
    
    search = request.GET.get("search")
    limit = int(request.GET.get("limit"))
    offset = int(request.GET.get("offset"))

    length = len(Question.objects.filter(subject__teacher=request.user)) 
    questions = Question.objects.filter(subject__teacher=request.user).filter(Q(subject__name__icontains=search) | Q(question__icontains=search)).values("id", "question","option_A", "option_B","option_C","option_D", "answer", "exam","subject", "subject__name", )
    
    if search:
        length =  len(questions)
    
    questions = questions[offset:limit+offset]
    return JsonResponse({"total":length, "rows":list(questions)})


def allQuestions(request):
    
    form = QuestionForm(request)
    subjects = Subject.objects.filter(teacher= request.user)
    
    context = {
        "form":form,
        "subjects": subjects
    }
    
    return render(request, "teachers/all_questions.html", context)

def is_ajax(request): #check if a call is an ajax call
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def createQuestion(request):  
    if is_ajax(request=request):
        form = QuestionForm(request, request.POST)
        if form.is_valid:
            form.save()
            return JsonResponse({"message":"added"})
        else:
            return JsonResponse({"message":form.errors})
        
def deleteQuestion(request):
    if is_ajax(request=request):
        ids = json.loads(request.POST.get("id"))
        quest = Question.objects.filter(id__in = ids)
        quest.delete()
        return JsonResponse({"deleted": True})
    
def editQuestion(request):
    if is_ajax(request=request):
        id = request.POST.get("id")
        question = Question.objects.get(id=id)
        form = QuestionForm(request, request.POST, instance=question)
        if form.is_valid:
            form.save()
            return JsonResponse({"res":"added"})
        else:
            print("No")
            return JsonResponse({"res":form.errors})
        
    