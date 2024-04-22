import imp
from logging import exception
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import exam
from users . models import User, Student
from teachers. forms import UserUpdateForm, ChangeProfilePicture
from students.forms import StudentUpdateForm, studentPasswordReset
from django.contrib import messages
from django.contrib.auth import authenticate, login
from exam . models import Exam
from django.core.paginator import Paginator
from django.http import JsonResponse
from random import shuffle
from exam . models import Question, Session
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from main.decorators import student
from django.contrib.auth.hashers import make_password







# Create your views here.
@student
@login_required
def profile(request):
    user = User.objects.get(username = request.user.username)
    changePassword = studentPasswordReset(request.user, request.POST or None)
    if request.method == "POST":
        changePassword = studentPasswordReset(request.user, request.POST)
        if changePassword.is_valid():
            password = request.POST.get("new_password1")
            user.set_password(password)
            user.save()
            messages.success(request, "Password successfully changed. Please login to confirm password")
            return redirect("login")
        else:
            messages.error(request, "Password wasn't changed. Please check form for errors")
            print("I am not valid")
    context = {
        "user": user,
        "changePassword": changePassword
    }
    return render(request, "students/profile.html", context)

@student
@login_required
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    p_form = UserUpdateForm(request, instance = user)
    s_form = StudentUpdateForm(instance= user.student)
    
    if request.method == "POST":
        p_form = UserUpdateForm(request, request.POST, instance = user)
        s_form = StudentUpdateForm(request.POST, instance= user.student)
        
        
        if p_form.is_valid() and s_form.is_valid():
            p_form.save()
            s_form.save()
            messages.success(request, "Profile updated")
            return redirect("student-profile")
    context ={
        "p_form":p_form,
        "s_form":s_form, 
    }
    return render(request, "students/edit_profile.html", context)

@student
@login_required
def editStudentProfileImage(request, pk):
    student = Student.objects.get(id=pk)
    form = ChangeProfilePicture(instance=student)
    if request.method == "POST":
        form = ChangeProfilePicture(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("edit-student-profile", pk=request.user.id)
    context ={
        "form":form
    }
    
    return render(request, "teachers/image.html", context)

@student
@login_required
def exams(request):
    """Exams that are ready and students are eligible to see and write"""
    exams = Exam.objects.filter(Q(start_date__lte=timezone.now(), end_date__gt=timezone.now()),
                                 ready=True, grade=request.user.student.grade).order_by("end_date")
    
    
    if request.method == "POST": #if the student clicks the start button on the modal in the available exam page
        id = request.POST.get("exam")
        if Session.objects.filter(user=request.user, exam=id).exists(): #check if the user has written this test before
            student_session = Session.objects.get(user=request.user, exam=id)
            if student_session.attempts < 2 or student_session.completed == False: # check if the student completed this exam even in his last attempt or how many times the user wrote this test (this student is eligible)
                request.session['id'] = id # add the exam.id to the session header because student is eligible to write
                if student_session.completed: # user wants to retake this test
                    request.session['check_storage_for_data'] = 0 # tell Javascript whether to check storage
                else: # user didn't finish the test
                    request.session['check_storage_for_data'] = 1 # tell Javascript whether to check storage
                return JsonResponse({"message": True})# True meaning you can open a new window
            
            else: #user has exceeded maximum attempts (this student is not eligible)
                # delete session variables if it exist to prevent accessing exam
                
                if request.session.get("check_storage_for_data", None) != None:
                    if request.session['check_storage_for_data'] != None: 
                        del request.session['check_storage_for_data'] 
                if request.session.get("id", None) != None:
                    if request.session['id'] != None:
                        del request.session['id']
                return JsonResponse({"message": False}) # True meaning you can open a new window
            
        else: #first time writers
            request.session['id'] = id # add the exam.id to the session header
            request.session['check_storage_for_data'] = 0 # tell Javascript whether to check storage
            return JsonResponse({"message": True})
     
    context ={
        "exams": exams
    }
    return render(request, "students/available_exam.html", context)

@student
@login_required
def session(request):  #this is the exam page
    id = request.session.get('id')  #-------------------- bug -------------------- if student hard refreshes the page, the exam will be lost
    check_storage_for_data = request.session.get('check_storage_for_data')  #-------------------- bug -------------------- if student hard refreshes the page, the exam will be lost
    
    
    if id ==None or check_storage_for_data==None: #if the user copied the url, the user is without a value id, hence raise a permission error
        return redirect("available-exam")
        # raise PermissionDenied
    
    exam = Exam.objects.get(id= id)
        
    if Session.objects.filter(user=request.user, exam=id).exists(): # if the user has a pk in the db and refreshes the page, run this code
        student_session = Session.objects.get(user=request.user, exam=id)
        if  student_session.attempts <2 or student_session.completed == False: # if no. of attempt == 2 del the exam.id from session header
            
            if student_session.completed: # user wants to retake this test
                request.session['check_storage_for_data'] = 0 # tell Javascript whether to check storage
            else: # user didn't finish the test
                request.session['check_storage_for_data'] = 1 # tell Javascript whether to check storage
            
        else:
            del request.session['id']
            del request.session['check_storage_for_data']
            return redirect("available-exam")
        
    
            
    context = {
        "exam": exam
    }
    return render(request, "students/exam_page.html", context)

def session_data(request, pk):
    # student questions
    exam = get_object_or_404(Exam, pk=pk)
    if is_ajax(request=request):
        session , created = Session.objects.get_or_create(user= request.user, exam=exam)
                
        if session.attempts < 2:
            questions = Question.objects.filter(exam=exam).values()
            
            data_ =[]
            prechoices = {} #to avoid getting keyerror if a student doesn't complete the exam and the exam has ended
            
            for question in questions:
                prechoices[question["question"]] = [""]
                options = [ question["option_A"], question["option_B"], question["option_C"], question["option_D"] ]
                zipper =dict(list( zip(['A', 'B', 'C', 'D'], options)))
                answer_Abbrv =  question["answer"] # the answer in the database e.g "C"
                shuffle(options)
                data_.append({question["question"]:options, "answer": zipper[answer_Abbrv]})
            shuffle(data_)
            data ={"data":data_, 
                   "time":exam.duration.total_seconds(),
                   "attempts": session.attempts, 
                #    "allow_retake":exam.retake, 
                   "allow_correction":exam.review,
                   "user": request.user.get_full_name()}
            
            session.choices = prechoices
            session.time_started = timezone.now()
            session.completed = False
            # session.attempts = session.attempts +1
            session.save()
            
            return JsonResponse(data)
        else:
            return JsonResponse({"data":False})  #exams has already been written
    else:
        raise PermissionDenied  #someone is trying to see the data through a get method
    
def is_ajax(request): #check if a call is an ajax call
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
 
def session_save(request, pk):
    if is_ajax(request=request):  
        user = request.user
        exam = Exam.objects.get(id=pk) 
        user_session = Session.objects.get(user=user, exam = exam)
        db_attempts = user_session.attempts #attempts before the session ended
        questions = []
        data =  request.POST
        data_ =dict(data.lists()) #lists() is only available for request.POST method-->, The lists method returns a list of tuples containing the names and values of the input fields.
        ######################################
        data_.pop("csrfmiddlewaretoken") #remove the csrf_token from the dictionary for us to manipulate the question
        elapsed = data_.pop("elapsedTime")[0]
        # attempts= int(data_.pop("attempts")[0])
        misconduct = True if data_.pop("misconduct")[0] == "true" else False
        attempts_= 2 if misconduct else db_attempts
        # attempts_ = 2 if (attempts+ db_attempts) > 2 else attempts + db_attempts
        ######################################
        
        for k in data_.keys():
            question = Question.objects.get(question = k)
            questions.append(question) # appending question object in a list

        
        score = 0
        multiplier = 100 / exam.question_set.all().count()
        results = []
        correct_answer = []
        
        for q in questions:  # q is the question instance
            a_selected = data_.get(q.question) #from the question instance get the question key from the request.POST method
            answer  = {"A" :q.option_A, "B":q.option_B, "C":q.option_C, "D":q.option_D} # represent the options as "A", "B", "C", "D" to correspond to the correct answer from the db
    
            if a_selected[0] != "": # if what the user selected is not empty
                for option, value in answer.items(): # from the answers in the db as dictionary
                    if a_selected[0] in value: # if the student_answer in list of answers (value)
                        if option == q.answer: # if the option is == the teacher answer
                            data_.get(q.question).append({"status": "correct"}) #---------------
                            score += 1  # add a mark
                            correct_answer.append(value) # the student was correct
                        else:
                            data_.get(q.question).append({"status": "incorrect"}) #---------------
                            correct_answer.append(answer[str(q.answer)]) #the student answer was not correct. Put the correct answer
            else:
                data_.get(q.question).append({"status": "unanswered"}) #---------------
                correct_answer.append(answer[str(q.answer)])
            #     results.append({str(q):{"correct_answer": correct_answer, "answered": a_selected}}) # create dictionary of correct and not correct answer
            # else:
            #     results.append({str(q): "not answered"}) # if the question was not answered create a not answered dictionary
                
        score_ = round(score * multiplier ,1)# convert to 100% scale
        user_session.exam = exam
        user_session.score=score_
        user_session.elapsed_time=elapsed
        user_session.attempts=attempts_
        user_session.misconduct=misconduct
        user_session.completed = True
        user_session.choices = data_
        user_session.save()
        
        # Session.objects.create(user=user, exam = exam, score=score_, elapsed_time=elapsed, attempts=attempts, misconduct=misconduct ) # create and instance of this user session
        
        if score_>=exam.pass_mark:
            return JsonResponse({"pass": True, "score": score_, "no_of_correct_answer":score, "correctAnswers": correct_answer})
            # return JsonResponse({"pass": True, "score": score_, "result":results}) # create a json response for this user to display data
        else:
            return JsonResponse({"pass": False, "score": score_, "no_of_correct_answer":score, "correctAnswers": correct_answer})
           # return JsonResponse({"pass": False, "score": score_, "result":results}) # create a json response for this user to display data
    else:
        raise PermissionDenied


@student
@login_required  
def examResult(request):
    exams = Exam.objects.filter(end_date__lt=timezone.now(), grade=request.user.student.grade).order_by("end_date")
    
    sessions = Session.objects.filter(Q(exam__end_date__lt=timezone.now(), exam__grade=request.user.student.grade), user = request.user)
    
    context={
        "exams":exams, 
        "sessions":sessions
    }
    return render(request, "students/exam_result.html", context)


def examAnalysis(request, pk):
    session = Session.objects.get(id=pk)
    context ={
        "session": session,
        "pk": session.id,
        "score": session.score,
        "no_quest": len(session.choice)
    }
    return render(request, "students/exam_analysis.html", context)


def  sessionCorrectionData(request, pk):
    session = Session.objects.get(id=pk)
    questions = Question.objects.filter(exam=session.exam.id)
    # questions = serializers.serialize("json", questions, fields=("question", "option_A", "option_B", "option_C", "option_D"))
    
    data = []
    for question in questions:
        question_and_options = {}
        options = {"A":question.option_A, "B": question.option_B, "C":question.option_C, "D": question.option_D}
        question_and_options["question"] = question.question
        question_and_options["options"] = [options]
        question_and_options["answer"] = options[question.answer]
        question_and_options["choice"] = session.choices[question.question][0]
        data.append(question_and_options)
    return JsonResponse({"data": data})
              
            

        
    