from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import *
from . models import User, Student
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user}")
            return redirect("lobby")
        else:
            messages.error(request, "Username or Password is not correct")
        
    context = {
        "page": "login"
    }
    return render(request, "login_registration.html", context)

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def lobby(request):
    """
    Handles requests from both students and teachers.
    
    If the user is a teacher and their status is "Approved", they are redirected to the "home" page.
    If the user is a student and their status is "Approved", nothing happens.
    If the user is neither a teacher nor a student, nothing happens.
    
    If the user is a student, the function creates a form for student requests and handles the form submission.
    If the form is valid, a new `Student` object is created and saved to the database.
    
    If the user is a teacher, the function creates a form for teacher requests and handles the form submission.
    If the form is valid, a new `Teacher` object is created and saved to the database.
    
    Finally, the function renders the "lobby.html" template with the appropriate form.
    
    Args:
        request (HttpRequest): The HTTP request object containing information about the current request.
        
    Returns:
        None
    """
    try:
        if request.user.teacher.status == "Approved":
            return redirect("home")
        elif request.user.student.status == "Approved":
            pass
    except ObjectDoesNotExist:
        pass
    
        
    if request.user.is_student:
        form = StudentRequestForm(request, data=request.POST or None, files=request.FILES or None)
        if request.method =="POST":
            form = StudentRequestForm(request, request.POST, request.FILES)
            if form.is_valid():
                birth = form.cleaned_data["birth"]
                gender = form.cleaned_data["gender"]
                image = form.cleaned_data["image"]
                
                try:
                    student = Student.objects.create(user = request.user,birth = birth,gender = gender)
                except IntegrityError:
                    messages.info(request, "Profile already submitted, which is now pending admin verification")  
                else:
                    student.image=image
                    student.save()  
                    messages.success(request, "Created successfully") 
                return redirect("lobby")
    else:
        form = TeacherRequestForm(request, data=request.POST or None, files=request.FILES or None)
        if request.method =="POST":
            form = TeacherRequestForm(request, request.POST, request.FILES)
            if form.is_valid():
                phone = form.cleaned_data["phone"]
                gender = form.cleaned_data["gender"]
                email = form.cleaned_data["email"]
                image = form.cleaned_data["image"]
                
                try:
                    teacher = Teacher.objects.create(user = request.user,phone = phone,gender = gender, email=email)
                except IntegrityError:
                    messages.info(request, "Profile already submitted, which is now pending admin verification")  
                else:
                    teacher.image=image
                    teacher.save()  
                    messages.success(request, "Created succesful") 
                return redirect("lobby")
    
    
    context ={
        "form": form,
    }
    return render(request, "lobby.html", context)

def home(request):
    
    return render(request, "index.html")


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():   
            role = form.cleaned_data.get("role")
            user = form.save(commit=False)
            if role == "student":
                user.is_student = True
            else:
                user.is_teacher = True
            
            user.save()
            messages.add_message(request, messages.SUCCESS, "User created")
            return redirect("login")
    context = {
        "form": form
    }
    return render(request, "login_registration.html", context)