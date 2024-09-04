from tabnanny import verbose
from django.db import models

from school.models import Grade, Level, Subject


        
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete= models.CASCADE, null=True)
    name = models.CharField(max_length=225)
    
    class META:
        ordering = ("subject__name","name")
        
    def __str__(self) :
        return self.name
    
    