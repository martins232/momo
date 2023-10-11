from django.core.exceptions import PermissionDenied


def teacher(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_teacher==True and request.user.teacher.status == "Approved":
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper