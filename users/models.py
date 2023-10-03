from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
STATUS_CHOICE = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected")
)


class User(AbstractUser):
    is_student = models.BooleanField(null=True)
    is_teacher = models.BooleanField(null=True)
    is_superteacher = models.BooleanField(null=True)
    
    
    
    def __str__(self):
        return self.username
    
    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Birthday")
    gender = models.CharField(max_length=10)
    image = models.FileField(upload_to="photo", blank=True, verbose_name="Photo")
    # status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICE, default="Pending")
    # grade=
    
    def __str__(self):
        return self.user.username