from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date




# Create your models here.
STATUS_CHOICE = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected")
)
class Grade(models.Model):
    grade = models.IntegerField()
    
    
    class Meta:
        ordering = ["grade"]
    
    def __str__(self):
        return f"Grade {str(self.grade)}"

class User(AbstractUser):
    is_student = models.BooleanField(null=True)
    is_teacher = models.BooleanField(null=True)
    is_superteacher = models.BooleanField(null=True)
    
    REQUIRED_FIELDS =["first_name", "last_name"]
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    birth = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Birthday")
    gender = models.CharField(max_length=10)
    image = models.FileField(upload_to="photo", verbose_name="Photo", default="/media/photo/avatar.jpg")
    status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICE, default="Pending")
    
    @property
    def get_age(self):
        birth_day = self.birth
        age = int((date.today() - birth_day).days / 365)
        return age
        
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.FileField(upload_to="photo",blank=True, verbose_name="Photo",)
    status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICE, default="Pending")
    
    
    def __str__(self):
        return self.user.username
    
    # def save(self, *args, **kwargs):
    #     if self.status == "Approved":
    #         self.user.is_staff = True
    #     super(Teacher, self).save(*args, **kwargs)