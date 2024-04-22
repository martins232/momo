import json
from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher, Grade
from main . decorators import teacher
from teachers. forms import UserUpdateForm,TeacherUpdateForm, ChangeProfilePicture, TopicForm
from django.contrib.auth.decorators import login_required
from exam.forms import ExamForm, QuestionForm
from django.contrib import messages
from exam .models import Exam, Question, Session
from teachers.models import Subject, Topic
from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.http.response import JsonResponse
from django.db.models import Count, Avg



from django.utils import timezone



from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

# Create your views here.
@login_required(login_url="login")
def userProfile(request):
    user = User.objects.get(username = request.user.username)
    subjects = Subject.objects.filter(teacher=user)
    context = {
        "user": user,
        "subjects":subjects,
        "count_course" : subjects.count()
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
def scheduledExam(request):
    #form to create exam
    form = ExamForm(request, request.POST or None)
    
    #get all the exams by this teacher
    # exams = Exam.objects.filter(teacher=request.user, )
    exams = Exam.objects.filter( Q(start_date__gt=timezone.now()) | Q(start_date__lte=timezone.now(), end_date__gt=timezone.now()), teacher=request.user)
    
    #all the classes 
    grades = Grade.objects.filter(Q(exam__start_date__gt=timezone.now()) | Q(exam__start_date__lte=timezone.now(), exam__end_date__gt=timezone.now()), exam__teacher=request.user).distinct()
    if request.method == "POST":
        form = ExamForm(request, request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.add_message(request, messages.SUCCESS, "Exam created")
            return redirect("scheduled-exam")
        else:
            messages.add_message(request, messages.ERROR, form.errors.as_ul())   
    context = {
        "form": form,
        "exams": exams,
        "grades": grades,
    }
  
    return render(request, "teachers/schedule_exam.html", context)

def closedExam(request):
    """Exams that have been completed"""
    grades = Grade.objects.filter(exam__end_date__lt=timezone.now(), exam__teacher=request.user).distinct()
    exams = Exam.objects.filter(end_date__lt=timezone.now(), teacher=request.user)
    
    context = {
        "exams": exams,
        "grades": grades
        }
    return render(request, "teachers/closed_exam.html", context)

@teacher
@receiver(post_save, sender=Subject)
def set_exam_teacher_null(sender, instance, **kwargs):
    """
    This function is used to transfer subsject, exams and question from one teacher to another
    """
    # instance is the subject object that was deleted
    # get the exams that are related to this subject
    exams = Exam.objects.filter(subject=instance) #all the exams by the new teacher of this subject
    # # # loop through the exams and set their teacher to null
    for exam in exams:
        exam.teacher = instance.teacher
        exam.save()
        
        # for question in questions:
        #     question.teacher = instance.teacher
        #     question.save()
        #     print(question)
        
@teacher
@login_required(login_url="login")
def deleteExam(request):
    if is_ajax(request=request):
        id = request.POST.get("id")
        exam = get_object_or_404(Exam, id=id)
        exam.delete()
        return JsonResponse({"message": "deleted"})
        
    else:
        raise PermissionDenied
        
    
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
            name= form.cleaned_data["name"]
            form.save()
            messages.add_message(request, messages.SUCCESS, "Exam saved")
            return redirect("scheduled-exam")
        
    context = {
        "form": form,
        "obj_name": "EXAM"
    }  
    return render(request, "teachers/edit.html", context) 



    

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
        
        options = {"A" :question.option_A, "B" :question.option_B, "C" :question.option_C, "D" :question.option_D,} #{"A":"........"}
        #dict to get number of student that chose an option
        option_choice_nos={question.option_A:0, question.option_B:0, question.option_C:0, question.option_D:0} #{"......":0}
        
        for session in sessions:
            student_choice = session.choices[question.question][0]
            if student_choice == "":
                unanswered_count += 1
                unanswered_student[str(session.user.id)] = str(session.user.get_full_name())
            else:
                option_choice_nos[student_choice]+=1
                if student_choice == options[question.answer]:
                    correct_count +=1
                    correct_student[str(session.user.id)] = str(session.user.get_full_name())
                if student_choice != options[question.answer]:
                    incorrect_count +=1
                    incorrect_student[str(session.user.id)] = session.user.get_full_name()
            
        data.append({
            "question": question.question, 
            "correct": correct_count, 
            "incorrect": incorrect_count, 
            "unanswered": unanswered_count,
            "correct_student": correct_student,
            "incorrect_student": incorrect_student,
            "unanswered_student": unanswered_student,
            "option_count" : option_choice_nos
            })
      
            
    
    
    return JsonResponse({"rows":data})

def newExamDashboard(request, pk):
    exam = Exam.objects.get(id = pk)
    sessions = Session.objects.filter(exam= exam).order_by("-score")
    context ={
        "exam":exam,
        "sessions":sessions,
    }
    return render(request, "teachers/new_exam_dashboard.html", context)
  
    
#dashboard after exams has been taken  
def examDashboard(request, pk):
    exam = Exam.objects.get(id = pk)
    sessions = Session.objects.filter(exam= exam).order_by("-score")
    context ={
        "exam":exam,
        "sessions":sessions,
        "pk": pk
    }
    
       
    return render(request, "teachers/exam_dashboard.html", context)


def questionData(request):
    
     # for the sake of other subjects that would use this JSON data
    subject_list = Subject.objects.filter(teacher=request.user) # used in the all_question page to filter all questions by a particular teacher 
    
    subject = request.GET.get("subject") # used in the drag page to filter questions for a particular subject 
    search = request.GET.get("search") 
    limit = int(request.GET.get("limit"))
    offset = int(request.GET.get("offset"))
    unassigned = request.GET.get("unassigned")
    exam_id = request.GET.get("exam")
    # unassigned = bool(int(request.GET.get("unassigned", 0)))
    
    
    
    # if a particular subject that is making the request through ajax
    if subject != None:
        subject_list = list(subject)
    

    length = Question.objects.filter(subject__in=subject_list).count() #get all the questions by the logged in teacher
    questions = Question.objects.filter(subject__in=subject_list).filter(Q(subject__name__icontains=search) | Q(question__icontains=search)).values("id", "question","option_A", "option_B","option_C","option_D", "answer", "exam","exam__name","subject", "subject__name", )
    
    
    
    
    
    if search:
        length =  questions.count()
        
    if unassigned is not None: # if the teacher wants filter between unassigned  and assigned questions
        unassigned = bool(int(unassigned))
        if unassigned:
            questions = questions.filter(exam__isnull = unassigned)
            length =  questions.count()
        else:
            questions = questions.filter(exam__isnull = unassigned)
            length =  questions.count()
    
    if exam_id != None and unassigned==False: #to get just assigned topic to a particular exam
        questions = questions.filter(exam = exam_id)
        length =  questions.count()
       
    questions = questions[offset:limit+offset]
    return JsonResponse({"total":length, "offset": offset, "rows":list(questions)})


def is_ajax(request): #check if a call is an ajax call
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def createQuestion(request):  
    if is_ajax(request=request):
        form = QuestionForm(request, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"added"})
        else:
            errors = form.errors 
            return JsonResponse({"message": "Validation errors", "errors": errors})
            
        
def deleteQuestion(request):
    if is_ajax(request=request):
        ids = json.loads(request.POST.get("id"))
        quest = Question.objects.filter(id__in = ids)
        a = quest.delete()
        return JsonResponse({"deleted": True})
    
def editQuestion(request):
    if is_ajax(request=request):
        id = request.POST.get("id")
        question = Question.objects.get(id=id)
        form = QuestionForm(request, request.POST, instance=question)
        if form.is_valid():
            form.save()
            return JsonResponse({"res":"added"})
        else:
            errors = form.errors 
            return JsonResponse({"message": "Validation errors", "errors": errors})
        
        
        
def viewExam(request, pk):
    exam = Exam.objects.get(id=pk)
    context = {"exam": exam} #used for sending subject id in the templated
  
    return render(request, "teachers/view_exam.html", context)

def assignQuestionToExam(request, pk):
    exam = Exam.objects.get(id=pk)
    if is_ajax(request=request):
        ids = json.loads(request.POST.get("id"))
        questions = Question.objects.filter(id__in = ids)
        questions.update(exam=pk)
        
        if exam.get_no_question > 0:
            exam.ready = True
            exam.save()
        return JsonResponse({"message": f"{len(ids)} Question(s) added to {exam.name}. <br>Total questions: <span class='fw-bold'>{exam.get_no_question}</span>"})
    
def removeQuestionFromExam(request, pk):
    exam = Exam.objects.get(id=pk)
    if is_ajax(request=request):
        ids = json.loads(request.POST.get("id"))
        questions = Question.objects.filter(id__in = ids)
        questions.update(exam=None)
        
        if exam.get_no_question < 1:
            exam.ready = False
            exam.save()
        
        
        return JsonResponse({"message": f"{len(ids)} Question(s) removed from {exam.name}. <br>Total questions: <span class='fw-bold'>{exam.get_no_question}</span>"})

def topicsData(request):
    teacher = request.user
    subject = Subject.objects.filter(teacher = teacher)
    data = {}
    grade = request.GET.get("grade") 
    
    
    if grade is not None:
        for sub in subject:
            data[sub.name] = list(Topic.objects.filter(subject=sub, grade=grade).values("grade","id", "subject", "name"))
    return JsonResponse(data)

def allTopics(request):
    form = TopicForm(request)
    grades = Grade.objects.all()
    # subjects = Subject.objects.filter(teacher = request.user)
    context = {
        "form": form,
        "grades": grades
        }
    
    return render(request, "teachers/topics.html", context)

def addTopic(request):
    if is_ajax(request=request):
        form = TopicForm(request, request.POST)
        if form.is_valid():
            topic = form.save()
            msg = topic.subject.name + " for " + str(topic.grade)
            return JsonResponse({"message": f"New topic created in {msg}"})
        else:
            return JsonResponse({"message":"No"})
        
def editTopic(request):
    if is_ajax(request=request):      
        topic_id = request.POST.get("id")
        topic = get_object_or_404(Topic, id=topic_id)       
        form = TopicForm(request, request.POST, instance= topic)
        if form.is_valid():
            topic =form.save()
            msg = topic.subject.name + " for " + str(topic.grade)
            return JsonResponse({"message": f"Topic updated in {msg}"})
        else:
            return JsonResponse({"message": form.errors})


def deleteTopic(request):
    if is_ajax(request=request):
        id = request.POST.get("id")
        topic =Topic.objects.get(pk=id)
        if topic:
            msg = topic.subject.name + " for " + str(topic.grade)
            topic.delete()
            return JsonResponse({"message":f"Topic deleted from {msg}"})
        else:
            return JsonResponse({"message":"Something went wrong"})
        

#-------------------------------------------------------------
@teacher
@login_required(login_url="login")
def allQuestions(request):
    
    
    form = QuestionForm(request)
    subjects = Subject.objects.filter(teacher= request.user)
    context = {
        "form":form,
        "subjects": subjects, 
    }
    
    return render(request, "teachers/all_questions.html", context)

# @cache_page(60*15)
def question_create(request):
    data = dict()
    form = QuestionForm(request, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            print(form.errors)
            data['form_is_valid'] = False
            data['html_form'] = form
    context = {'form': form}
    data['html_form'] = render_to_string('teachers/includes/create_question.html',context,request=request)
    return JsonResponse(data)

    

# # @cache_page(60*15)
def question_edit(request, pk):
    question = Question.objects.get(id=pk)
    data = dict()
    form = form = QuestionForm(request, request.POST or None, instance=question)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
            data['html_form'] = form
    context = {'form': form}
    data['html_form'] = render_to_string('teachers/includes/create_question.html',context,request=request)
    return JsonResponse(data)

def question_delete(request):
    data= dict()
    
   
    # data = quest.delete()
    
    
    if is_ajax(request=request):
        if request.method == "POST":
            ids = json.loads(request.POST.get("id"))
            questions = Question.objects.filter(id__in =ids)
            deleted_question = questions.delete()
            print(deleted_question)
            data["deleted"] = True
            return JsonResponse(data)
        else:
            ids = request.GET.get("id").split(',')
            questions = Question.objects.filter(id__in =ids)
            context = {'questions': questions}
            data['html_form'] = render_to_string('teachers/includes/delete_question.html',context, request=request)
            return JsonResponse(data)
    