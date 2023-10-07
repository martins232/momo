from django.shortcuts import render, redirect, get_object_or_404
from users.models import User, Teacher
from . forms import TeacherUpdateForm
from django.contrib.auth.decorators import login_required
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