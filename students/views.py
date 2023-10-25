from django.shortcuts import render, redirect, get_object_or_404
from users . models import User, Student
from teachers. forms import UserUpdateForm, ChangeProfilePicture
from students.forms import StudentUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from exam . models import Exam
from django.core.paginator import Paginator

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

def session(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.question_set.all()
    
    p = Paginator(questions, 1)
    page_number = request.GET.get("page", 1)
    page = p.page(page_number)
    
    if not request.session.get("answers"):
        # Create an empty dictionary and assign it to request.session["answers"]
        request.session["answers"] = {}
    
    if request.method == "POST":
        # Get the name and value of the radio input from request.POST
        # name = request.POST.get("p")
        # value = request.POST.get("value")
        print(request.POST["answer"])
        # print(name, value)
        # Update the request.session["answers"] dictionary with the question id and answer
        # request.session["answers"][name] = value
        # # Redirect to the same URL with the page number as a query parameter
        # return redirect(f"{request.path}?page={page_number}")

    context = {
        
        "pk":exam.id,
        "questions": page,
        
    }
    return render(request, "students/session.html", context)