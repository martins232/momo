from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from users . models import User, Student
from teachers. forms import UserUpdateForm, ChangeProfilePicture
from students.forms import StudentUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from exam . models import Exam
from django.core.paginator import Paginator
from django.http import JsonResponse
from random import shuffle
from exam . models import Question, Session
from django.core.exceptions import PermissionDenied



# Create your views here.

def profile(request):
    user = User.objects.get(username = request.user.username)
    context = {
        "user": user,
    }
    context = {
        
    }
    return render(request, "students/profile.html", context)

def editProfile(request, pk):
    user = User.objects.get(id=pk)
    p_form = UserUpdateForm(request, instance = user,)
    s_form = StudentUpdateForm(instance= user.student)
    
    if request.method == "POST":
        p_form = UserUpdateForm(request, request.POST, instance = user,)
        s_form = StudentUpdateForm(request.POST, instance= user.student)
        
        if p_form.is_valid() and s_form.is_valid():
            p_form.save()
            s_form.save()
            messages.success(request, "Profile updated")
            return redirect("student-profile")
    context ={
        "p_form":p_form,
        "s_form":s_form
    }
    return render(request, "students/edit_profile.html", context)

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

def exams(request):
    exams = Exam.objects.filter(grade=request.user.student.grade)
    
     
    context ={
        "exams": exams
    }
    return render(request, "students/available_exam.html", context)

def session(request):
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get("exam"))
        value = request.POST.get("exam")
        request.session['value'] = value
    else:
        value = request.session.get('value')
        print("Value from GET: ",value)
        if not value:
            raise PermissionDenied
    
    return render(request, "students/exam_page.html")
def session_data(request, pk):
    if is_ajax(request=request):
        # if Session.objects.filter(user = request.user).exists():
        #     print("Yes")
        # else:
        #     print("Mo")
        exam = get_object_or_404(Exam, pk=pk)
        questions = exam.question_set.all().values()
        
        data_ =[]
        
        for question in questions:
            options = [ question["option_A"], question["option_B"], question["option_C"], question["option_D"], ]
            # shuffle(options)
            data_.append({question["question"]:options})
        shuffle(data_)
        data ={"data":data_, "time":exam.duration.total_seconds(), "user": request.user.username}
        return JsonResponse(data)
    else:
        raise PermissionDenied
    
def is_ajax(request): #check if a call is an ajax call
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
 
def session_save(request, pk):
    if is_ajax(request=request):     
        questions = []
        data =  request.POST
        data_ =dict(data.lists()) #lists() is only available for request.POST method-->, The lists method returns a list of tuples containing the names and values of the input fields.
        data_.pop("csrfmiddlewaretoken") #remove the csrf_token from the dictionary for us to manipulate the question
        elapsed = data_.pop("elapsedTime")[0]
        print(elapsed)
        for k in data_.keys():
            question = Question.objects.get(question = k)
            questions.append(question) # appending question object in a list
        user = request.user
        exam = Exam.objects.get(id=pk)
        
        score = 0
        multiplier = 100 / exam.question_set.all().count()
        results = []
        correct_answer = None
        
        for q in questions:  # q is the question instance
            a_selected = request.POST.get(q.question) #from the question instance get the question key from the request.POST method
            answer  = {"A" :q.option_A, "B":q.option_B, "C":q.option_C, "D":q.option_D} # represent the options as "A", "B", "C", "D" to correspond to the correct answer from the db
            
            if a_selected != "": # if what the user selected is not empty
                for option, value in answer.items(): # from the answers in the db as dictionary
                    if a_selected in value: # if the student_answer in list of answers (value)
                        if option == q.answer: # if the option is == the teacher answer
                            score += 1  # add a mark
                            correct_answer = value # the student was correct
                        else:
                            correct_answer = answer[q.answer] #the student answer was not correct
            #     results.append({str(q):{"correct_answer": correct_answer, "answered": a_selected}}) # create dictionary of correct and not correct answer
            # else:
            #     results.append({str(q): "not answered"}) # if the question was not answered create a not answered dictionary
                
        score_ = score * multiplier # convert to 100% scale
        Session.objects.create(user=user, exam = exam, score=score_) # create and instance of this user session
        
        if score_>=exam.pass_mark:
            return JsonResponse({"pass": True, "score": score_, "elapsed time": elapsed})
            # return JsonResponse({"pass": True, "score": score_, "result":results}) # create a json response for this user to display data
        else:
            return JsonResponse({"pass": False, "score": score_, "elapsed time": elapsed})
           # return JsonResponse({"pass": False, "score": score_, "result":results}) # create a json response for this user to display data
    else:
        raise PermissionDenied
                
            
                
        
    