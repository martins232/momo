from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def teacher(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous == True:
            return redirect("login")
        if request.user.is_teacher==True and request.user.teacher.status == "Approved":
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper