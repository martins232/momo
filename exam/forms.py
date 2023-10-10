from django import forms
from .models import Exam
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
    