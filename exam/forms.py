
from django import forms
from .models import Exam, Question
from users.models import Grade
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError


class ExamForm(forms.ModelForm):
    
    grade = forms.ModelChoiceField(
        label = "Grader",
        empty_label="Select a grade",
        required=True,
        queryset= Grade.objects.all(),
        widget=forms.Select(
            attrs={
                "style": "font-size : 13px;",
                "class": "form-control",
                
            }
        )
        )
    
    def __init__(self, request, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = request.user.subject_set.all()
        self.fields["duration"].help_text = "<li>H:M:S</li>"
        self.fields["duration"].initial = "00:60:00"
        # This will work but when the form selects all teachers that have an active session
        # self.fields['teacher'].initial = request.user
        # self.fields['teacher'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Exam
        exclude = ["teacher"]
        
        help_text={"duration": "Duration (H:M:S)"}
        
        widgets ={
            # Birth date
            "start_date": forms.DateInput(
                attrs={
                     "style": "font-size:14px; cursor:pointer",
                     "type":"date",
                     "onkeydown":"return false", # Javascript prevent typing
                     "min": str(date.today())
                }
            ),
        }
    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration > timedelta(hours=6, minutes=00, seconds=00):
            raise ValidationError("Duration can't be greater than 6hours")
        elif duration < timedelta(minutes=1):
            raise ValidationError("Duration can't be less than 5minutes")
        else:
            return duration
    
    def clean_start_date(self):
        start_date= self.cleaned_data.get("start_date")
        two_weeks_from_now = datetime.now() + timedelta(days=14)
        if start_date.timestamp() >two_weeks_from_now.timestamp():
            raise ValidationError("The exam start date must be within a two-week window from the current date.")
        return start_date

class QuestionForm(forms.ModelForm):
    answer_choice =[
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]
    answer = forms.ChoiceField(widget=forms.RadioSelect,
        choices=answer_choice,)   
    
    
    class Meta:
        model = Question
        exclude = ("exam", 'teacher', 'updated', 'created')
        
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].widget.attrs.update({"rows":5,}) 
        fields= ('option_A', 'option_B', 'option_C', 'option_D', )
        for field in fields:
            self.fields[field].widget.attrs.update({
            "placeholder":f"Answer for {field}",
            "rows":2,
            "style":"border-radius: 9px;"}) 
        
    