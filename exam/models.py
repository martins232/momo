from django.db import models
from users. models import User, Grade
from teachers. models import Subject
  
    
    
# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    start_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["start_date", "created"]
    
    
class Question(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    exam = models.ForeignKey(Exam, on_delete=models.RESTRICT)
    question = models.TextField()
    option_A = models.TextField()
    option_B = models.TextField()
    option_C = models.TextField()
    option_D = models.TextField()
    answer =  models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
    
    
    
    