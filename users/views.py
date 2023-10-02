from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import *
from . models import User
from django.contrib.auth import authenticate, login

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


def lobby(request):
    context ={}
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
            return redirect("home")
    context = {
        "form": form
    }
    return render(request, "login_registration.html", context)