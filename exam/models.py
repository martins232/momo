from django.db import models
from users. models import User, Grade
from teachers. models import Subject

  

STATUS = [
    ("Active", "ACTIVE"), 
    ("Pending", "PENDING")
]
    
# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    pass_mark = models.FloatField(verbose_name="Pass mark", default=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=25, choices=STATUS, default="Pending")
    retake = models.BooleanField( default=False)
    review = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    @property
    def get_no_question(self):
        return self.question_set.all().count()
    
    class Meta:
        ordering = [ "created"]
    
    
class Question(models.Model):
    # teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT, blank=False)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
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
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    score = models.FloatField(default=0.0)
    elapsed_time = models.FloatField(null=True)
    attempts = models.IntegerField(default=0)
    misconduct = models.BooleanField(default=False)
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    choices = models.JSONField(default=dict)
    
    
    def __str__(self):
        return str(self.pk)
    
    @property
    def passed(self):
        if self.score > self.exam.pass_mark:
            return "Passed"
        else:
            return "Fail"
    
    
   