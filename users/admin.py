from django.contrib import admin
from . models import User, StudentRequest

# Register your models here.
admin.site.register(User)
admin.site.register(StudentRequest)