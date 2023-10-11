from django import forms
from .models import Exam, Question
from datetime import date


class ExamForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = request.user.subject_set.all()
        
        # This will work but when the form selects all teachers that have an active session
        # self.fields['teacher'].initial = request.user
        # self.fields['teacher'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Exam
        exclude = ["teacher"]
        
        labels={"duration": "Duration (H:M:S)"}
        
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
    

class QuestionForm(forms.ModelForm):
    
    
    class Meta:
        model = Question
        exclude = ('teacher', 'updated', 'created')