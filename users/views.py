from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import *
from . models import User, Student
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

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

@login_required(login_url="login")
def lobby(request):
    p_form = StudentRequestForm(request, data=request.POST or None, files=request.FILES or None)
    
    if request.method =="POST":
        form = StudentRequestForm(request, request.POST, request.FILES)
        if form.is_valid():
            birth = form.cleaned_data["birth"]
            gender = form.cleaned_data["gender"]
            image = form.cleaned_data["image"]
            
            try:
                student = Student.objects.create(
                    user = request.user,
                    birth = birth,
                    gender = gender,
                )
            except IntegrityError:
                messages.info(request, "Profile already submitted, which is now pending admin verification")  
            else:
                student.image=image
                student.save()  
                messages.success(request, "Created succesful") 
            return redirect("lobby")
    context ={
        "form": p_form
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
            messages.add_message(request, messages.INFO, "User created")
            return redirect("login")
    context = {
        "form": form
    }
    return render(request, "login_registration.html", context)