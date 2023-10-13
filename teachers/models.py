from django.db import models
from users.models import User

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=25, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"is_teacher":True})
    assigned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def clean_name(self):
        self.name = self.name.capitalize()
    
    def save(self, *args, **kwargs):
        self.clean_name
        if self.teacher is not None:
            self.assigned = True
        else:
            self.assigned= False
        super(Subject, self).save(*args, **kwargs)
       
    class Meta:
        ordering = ["name"]
    
    