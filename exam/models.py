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
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    