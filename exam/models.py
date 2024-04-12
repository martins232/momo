from email.policy import default
from tabnanny import verbose
from django.db import models
from users. models import User, Grade
from teachers. models import Subject
from django.utils import timezone

from django.contrib import admin



from datetime import date
# from django_ckeditor_5.fields import CKEditor5Field
  

STATUS = [
    ("active", "ACTIVE"), 
    ("pending", "PENDING")
]
    
# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    pass_mark = models.FloatField(verbose_name="Pass mark", default=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ready = models.BooleanField(default=False) #to make sure exam satisfy every requirements like no. of quest etc before students can see it
    retake = models.BooleanField( default=False)
    review = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.name
    
    
    
    @property
    def get_exam_status(self):
        now = timezone.localtime(timezone.now())
        startExam = timezone.localtime(self.start_date)
        endExam = timezone.localtime(self.end_date)

        if now < startExam:
            return "pending"
            
        if now> startExam  and now< endExam:
            return "active"
            
        if now> startExam and now> endExam:
            return "ended"

        #####################debuging###############################################
        # print("Current tz: ",timezone.get_current_timezone())
        # print("Current tz name: ",timezone.get_current_timezone_name())
        # print("Current time in UTC: ",timezone.now())
        # print("The time is: ",timezone.localtime(now))
        # print("The date is: ",timezone.localdate(now))
        # print("The Exam end date is: ",timezone.localtime(self.end_date))
        # print("The Exam end date is UTC: ",self.end_date)
        #####################debuging###############################################
        
                      
                                                    
    @property
    def get_no_question(self):
        return self.question_set.all().count()
    
    @property
    def seconds_to_hms(self):
        duration = self.duration.seconds
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        return f"{str(hours) + 'hr' if hours > 0 else ''} {'s' if hours>1 else ''} {str(minutes) + 'min ' if minutes > 0 else ''} {str(seconds) + 'sec(s)' if seconds > 0 else ''}"
    
    class Meta:
        ordering = [ "created"]
    
    
class Question(models.Model):
    # teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT, blank=False)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    # question = CKEditor5Field('Question')
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
    
    class Meta:
        ordering = [ "-created"]
    
    
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, default=1)
    # exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    score = models.FloatField(default=0.0)
    elapsed_time = models.FloatField(null=True)
    attempts = models.IntegerField(default=0)
    misconduct = models.BooleanField(default=False)
    time_started = models.DateTimeField(null=True)
    time_ended = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    choices = models.JSONField(default=dict)
    
    
    def __str__(self):
        return str(self.pk)
    
    @property
    def passed(self):
        if self.score >= self.exam.pass_mark:
            return "Passed"
        else:
            return "Fail"
        
    def seconds_to_hms(self):
      
        hours = int(self.elapsed_time // 3600)
        minutes = int((self.elapsed_time % 3600) // 60)
        seconds = int(self.elapsed_time % 60)
        
        
        return f"{str(hours) + 'h ' if hours > 0 else ''} {str(minutes) + 'm: ' if minutes > 0 else ''} {str(seconds) + 's' if seconds > 0 else ''}"
    
    
   