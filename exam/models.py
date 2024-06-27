from asyncio import constants
from collections import defaultdict
from turtle import mode
from urllib import request
from django.db import models
from users. models import User, Grade
from teachers. models import Subject, Topic
from django.utils import timezone
from django.db.models import UniqueConstraint,Q

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
    deleted = models.BooleanField(default=False)
    review = models.BooleanField(default=False)
    retake = models.BooleanField( default=False)
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

       
                      
                                                    
    @property
    def get_no_question(self):
        return self.question_set.all().count()
    
    @property
    def get_all_question(self):
        return self.question_set.all()
    
    @property
    def seconds_to_hms(self):
        duration = self.duration.seconds
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        return f"{str(hours) + 'hr' if hours > 0 else ''}{'s' if hours>1 else ''} {str(minutes) + 'min ' if minutes > 0 else ''} {str(seconds) + 'sec(s)' if seconds > 0 else ''}"
    
    def duration_to_minutes(self):
        duration = self.duration.seconds
        minutes = int(duration / 60)
        return minutes
        
        
        
    def topic_count(self):
        """
        Calculate the count of unique topics for the questions associated with the current exam instance.

        This method retrieves all questions related to the current exam instance and creates a dictionary
        with the names of the topics as keys and 0 as the value, indicating the initial count. It also
        compiles a list of question IDs that do not have an associated topic.

        Returns:
            dict: A dictionary with topic names as keys and 0 as the value for each key.
        """
        questions = self.question_set.all()
        topics_count = defaultdict(dict)
        questions_without_topic = list()
        for question in questions.select_related("topics"):
            if question.topics:
                topic_name = question.topics.name  # Assuming the Topic model has a 'name' field
                topics_count[topic_name] = {"correct": 0, "incorrect":0, "unanswered": 0, "no_questions":0}
            else:
                questions_without_topic.append(question.id)
        return dict(topics_count), questions_without_topic
    
    def delete(self, *args, **kwargs):
        # super(Exam).delete(*args, *kwargs)
        
        if self.get_exam_status in ["ended"]:
            sessions = self.session_set.exists()
            
            if (sessions):
                self.deleted = True
                self.save()
            else:
                super().delete(*args, **kwargs)
        else:
            super().delete(*args, **kwargs)              
        
    class Meta:
        ordering = [ "created"]           
        
    
    
class Question(models.Model):
    # teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_teacher":True})
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT, blank=False)
    # exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    exam = models.ManyToManyField(Exam,)
    topics = models.ForeignKey(Topic, on_delete=models.SET_NULL, blank=True, null=True)
    question = models.TextField(unique=True)
    option_A = models.TextField()
    option_B = models.TextField()
    option_C = models.TextField()
    option_D = models.TextField()
    answer =  models.CharField(max_length=250)
    explanation = models.CharField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ...
        # ordering = [ "-created"]
    
    
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,)
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
      
        if self.elapsed_time > 0:
            hours = int(self.elapsed_time // 3600)
            minutes = int((self.elapsed_time % 3600) // 60)
            seconds = int(self.elapsed_time % 60)
            
            
            return f"{str(hours) + 'h ' if hours > 0 else ''} {str(minutes) + 'm ' if minutes > 0 else ''} {str(seconds) + 's' if seconds > 0 else ''}"
        else:
            return "-"
    
    def get_correct_count(self):
        choices_data = self.choices
        correct = 0
        incorrect = 0
        unanswered = 0
        
        for option in choices_data.values():
            if option[1].get("status") == "correct":
                correct += 1
            elif option[1].get("status") == "incorrect":
                incorrect += 1
            elif option[1].get("status")== "unanswered":
                unanswered += 1
                    
        return correct, incorrect, unanswered


# class StudentAnswer(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice = models.CharField(max_length=255)
#     status = models.CharField(max_length=10)  # e.g., "correct", "incorrect", "unanswered"