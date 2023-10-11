from django.db import models
from users. models import User
from teachers. models import Subject

# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    start_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-updated", "created"]
    
    
class Question(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    question = models.TextField()
    option1 = models.CharField(max_length=250)
    option2 = models.CharField(max_length=250)
    option3 = models.CharField(max_length=250)
    option4 = models.CharField(max_length=250)
    answer =  models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
    
    
    
    