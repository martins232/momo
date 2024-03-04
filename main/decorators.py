from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def teacher(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous == True:
            return redirect("login")
        if request.user.is_teacher==True and request.user.teacher.status == "Approved":
            if request.GET.get("next") is None:
                return view_func(request, *args, **kwargs)    #if there is no GET= "next" parameter, carry  on with th func
            else:
                return redirect(request.GET.get("next")) #if the teacher bookmarked this page i.e if there is "next" get parameter    
        else:
            raise PermissionDenied
    return wrapper