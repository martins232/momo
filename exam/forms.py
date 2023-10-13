from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Exam, Question
from datetime import date


class ExamForm(forms.ModelForm):
    
    def __init__(self, request, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = request.user.subject_set.all()
        self.fields["duration"].help_text = "<li>H:M:S</li>"
        
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
        self.fields["question"].widget.attrs.update({"rows":4,}) 
        fields= ('option_A', 'option_B', 'option_C', 'option_D', )
        for field in fields:
            self.fields[field].widget.attrs.update({
            "placeholder":f"Answer for {field}",
            "rows":1,
            "style":"border-radius: 9px;"}) 
        
    