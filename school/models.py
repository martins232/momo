from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    motto = models.CharField(max_length=255, null=True)
    address = models.TextField()
    contact_numbers = models.CharField(max_length=50)  # Store multiple numbers as comma-separated values
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Level(models.Model):
    """Levels just like senoir secondary or Junior Secondary"""
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='levels', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Grade(models.Model):
    name= models.CharField(max_length=50, null=True)
    grade = models.IntegerField()
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    
    
    class Meta:
        ordering = ["grade"]
    
    def __str__(self):
        return self.name
        # return f"Grade {str(self.grade)}"
    

class Subject(models.Model):
    name = models.CharField(max_length=25, unique=True)
    teacher = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"is_teacher":True})
    assigned = models.BooleanField(default=False)
    grade = models.ManyToManyField(Grade, related_name="subject")
    
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





class AcademicYear(models.Model):
    """Represents a school session (e.g., 2023/2024)."""
    name = models.CharField(max_length=20, unique=True)  # e.g., "2023/2024"
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    is_current = models.BooleanField(default=False)  # Tracks if this is the current session

    def __str__(self):
        return f"{self.name} session"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one active session per school
            AcademicYear.objects.filter(school=self.school, is_current=True).update(is_current=False)
        
        super().save(*args, **kwargs)

    def clean(self):
        if self.is_current:
            # Check if another current session exists for the same school
            if AcademicYear.objects.filter(school=self.school, is_current=True).exclude(pk=self.pk).exists():
                raise ValidationError("There can only be one active academic session for your school.")
        super().clean()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school'], condition=models.Q(is_current=True), name='unique_current_academic_year_per_school')
        ]
    
class Term(models.Model):
    """Represents a term within a school session."""
    name = models.CharField(max_length=50)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    # weeks = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return f"{self.name}"
    

    def clean(self):
        # Check for overlapping dates within the same academic year
        overlapping_terms = Term.objects.filter(
            academic_year=self.academic_year,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk)  # Exclude the current term from the check

        if overlapping_terms.exists():
            raise ValidationError(
                _("The dates for this term overlap with another term in the same academic year.")
            )

        # Ensure start date is before end date
        if self.start_date >= self.end_date:
            raise ValidationError(
                _("The start date must be before the end date.")
            )

        super().clean()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['academic_year', 'name'], name='unique_term_per_academic_year')
        ]