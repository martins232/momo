
from wsgiref.validate import validator
from django import forms
from .models import Exam, Question
from users.models import Grade
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError



# from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
# from django_ckeditor_5.widgets import CKEditor5Widget

from tinymce.widgets import TinyMCE


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
    start_date = forms.SplitDateTimeField(
        label='Start Date',
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            "style": "font-size:14px; cursor:pointer",
            "type":"date",
            # "onkeydown":"return false", # Javascript prevent typing
            # "min": str(date.today())
            }
        ,
       date_format='%Y-%m-%d',      
        time_attrs={
            'type':'time',
            "style": "font-size:14px; cursor:pointer",
            "class": "mt-3 w-50"
            },
        time_format='%H:%M',
        ))
    end_date = forms.SplitDateTimeField(
        label='End Date',
        widget=forms.SplitDateTimeWidget(
        date_attrs={
            "style": "font-size:14px; cursor:pointer",
            "type":"date",
            # "onkeydown":"return false", # Javascript prevent typing
            # "min": str(date.today() + timedelta(days=1)),
            
            },
       date_format='%Y-%m-%d',      
        time_attrs={
            'type':'time',
            "style": "font-size:14px; cursor:pointer",
            "class": "mt-3 w-50"
            },
        time_format='%H:%M',
        ))
    
    def __init__(self, request, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = request.user.subject_set.all()
        self.fields["duration"].help_text = "<li>H:M:S</li>"
        self.fields["retake"].label = "Allow students retake exam"
        self.fields["review"].label = "Allow students view correction after exam"
        self.fields["duration"].initial = "00:60:00"
        self.fields["name"].widget.attrs.update({"placeholder":"Enter exam name","style": "text-transform: capitalize;"})
        
        if self.instance:
            if self.instance.get_exam_status == "active":
                fields = ('grade',  'subject', 'duration', 'pass_mark', 'start_date','retake', 'review',)
                for field in fields:
                    self.fields[field].disabled = True
                
                self.fields["end_date"].widget.attrs.update({"min":str(date.today())})
        # This will work but when the form selects all teachers that have an active session
        # self.fields['teacher'].initial = request.user
        # self.fields['teacher'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Exam
        exclude = ["teacher", "ready"]
        
        help_text={"duration": "Duration (H:M:S)"}
    
    def clean_name(self):  
        return self.cleaned_data["name"].title()   
        
        
    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration > timedelta(hours=6, minutes=00, seconds=00):
            raise ValidationError("Duration can't be greater than 6hours")
        elif duration < timedelta(minutes=1):
            raise ValidationError("Duration can't be less than 5minutes")
        else:
            return duration
        
    def clean_end_date(self):
        start_date= self.cleaned_data.get("start_date")
        end_date= self.cleaned_data.get("end_date")
        
        if start_date >= end_date:
            raise ValidationError("The exam end date should be after the start date. Please adjust the end date to be a later date.")
        return end_date
    
    # def clean_start_date(self):
    #     start_date= self.cleaned_data.get("start_date")
    #     two_weeks_from_now = datetime.now() + timedelta(days=14)
    #     if start_date.timestamp() >two_weeks_from_now.timestamp():
    #         raise ValidationError("The exam start date must be within a two-week window from the current date.")
    #     return start_date

class QuestionForm(forms.ModelForm):
    answer_choice =[
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]
    # question =SummernoteTextField()
    # question =forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', "height":"220px"}}))
    answer = forms.ChoiceField(widget=forms.RadioSelect,
        choices=answer_choice,)   
    
    
    class Meta:
        model = Question
        exclude = ("exam", 'updated', 'created')
        # widgets = {
        #       "text": CKEditor5Widget(
        #           attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #       )
        #   }
        widgets = {
            'question': TinyMCE(attrs={"cols":80, "rows":30}),
        }
        
    def __init__(self,request,  *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # self.fields["question"].widget.attrs.update({"rows":5,}) 
        self.fields["question"].required = True
        self.fields['subject'].queryset = request.user.subject_set.all()
        self.fields["subject"].widget.attrs.update({'id': 'subject'})
        fields= ('option_A', 'option_B', 'option_C', 'option_D', )
        for field in fields:
            self.fields[field].widget.attrs.update({
            "placeholder":f"Answer for {self.fields[field].label}",
            "rows":2,
            "style":"border-radius: 9px;"}) 
            
    # def clean_question(self):
    #     if len(self.cleaned_data.get("question"))> 10:
    #         raise validator("I am testing things out bro")
    