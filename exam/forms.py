
from dataclasses import fields
from urllib import request
from wsgiref.validate import validator
from django import forms

from main.decorators import teacher
from .models import Exam, Question
from users.models import Grade
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from teachers.models import Topic
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

from .group_fields import GroupedModelChoiceField
from tinymce.widgets import TinyMCE

from django.utils.safestring import mark_safe

class CustomSplitDateTimeWidget(forms.SplitDateTimeWidget):
    
    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, datetime):
            value = [value.date(), value.time()]
        elif not value:
            value = [None, None]
        # Render the default SplitDateTimeWidget parts
        date_html = self.widgets[0].render(name + '_0', value[0] if value else None, attrs, renderer)
        time_html = self.widgets[1].render(name + '_1', value[1] if value else None, attrs, renderer)

        # Add the buttons to the date field
        date_html_with_buttons = f'''
        <div class="flatpickr-date input-group">
            {date_html}
            <button class="input-button btn btn-outline-secondary" type="button" title="toggle" data-toggle  >
                <i class="fas fa-calendar"></i>
            </button>
            
        </div>
        '''
        
        return mark_safe(date_html_with_buttons + time_html)



class MyRangeField(forms.DateField):
    # slider for duration field
    def to_python(self, value):
        if isinstance(value, timedelta):
            return value
        else:
            value = timedelta(minutes=int(value))
            return value
            
    
    
    
class ExamForm(forms.ModelForm):
    duration = MyRangeField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 10, 'max': 150, 'step': 5, "class":"form-range"})
    )
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
        widget=CustomSplitDateTimeWidget(
            date_attrs={
                "class": "flatpickr-input form-control",
                "placeholder": "Select Date..",
                "data-input": True,
                "style": "font-size:14px; cursor:pointer"
            },
            date_format='%Y-%m-%d',
            time_attrs={
                "class": "flatpickr-input form-control mt-3 w-50",
                "type": "time",
                "style": "font-size:14px; cursor:pointer"
            },
            time_format='%H:%M',
        )
    )
  
    
    
    
    end_date = forms.SplitDateTimeField(
        label='End Date',
        widget=CustomSplitDateTimeWidget(
            date_attrs={
                "class": "flatpickr-input form-control",
                "placeholder": "Select Date..",
                "data-input": True,
                "style": "font-size:14px; cursor:pointer"
            },
            date_format='%Y-%m-%d',
            time_attrs={
                "class": "flatpickr-input form-control mt-3 w-50",
                "type": "time",
                "style": "font-size:14px; cursor:pointer",
            },
            time_format='%H:%M',
        )
    )
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = request.user.subject_set.all()
        self.fields["duration"].help_text = "<span class='fw-bold'>1 hour</span>"
        self.fields["retake"].label = "Allow students retake exam"
        self.fields["review"].label = "Allow students see score after exam"
        self.fields["retake"].help_text = "<span class='fw-bold text-danger'></span>"
        self.fields["duration"].initial = "60"
        self.fields["name"].widget.attrs.update({"placeholder":"Enter exam name","style": "text-transform: capitalize;"})
        
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
        "name",
        'grade',
        'subject',
        'duration',
        'pass_mark',
        'start_date', 
        'end_date',
            Field('review', css_class="form-check-input", wrapper_class="form-check form-switch"),
            Field('retake', css_class="form-check-input", wrapper_class="form-check form-switch"),
            HTML("""
                <div class="modal-footer">
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-save"></i> Submit
                    </button>
                </div>
            """)
        )
        
        
        if self.instance.pk:
            self.fields["duration"].help_text = f"<span class='fw-bold'>{self.instance.seconds_to_hms}</span>"
            
            
            
            if self.instance.get_exam_status == "active":
                fields = ('grade',  'subject', 'duration', 'pass_mark', 'start_date','retake', 'review',)
                for field in fields:
                    self.fields[field].disabled = True
                
                self.fields["end_date"].widget.attrs.update({"min":str(date.today())})
            
            
            if self.instance.get_no_question > 0:
                self.fields["subject"].disabled = True
                
            
           
        
    class Meta:
        model = Exam
        exclude = ["teacher", "ready", "deleted"]
        
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
    
    def clean_review(self):
        retake = self.cleaned_data.get("retake")
        review = self.cleaned_data.get("review")
        
        if retake:
            if review == False:
                raise ValidationError("Allow students view score to decide if they want to retake an exam")
        else:
            return review
    
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
    # topics = GroupedModelChoiceField(
    #     queryset=Topic.objects.none(), 
    #     choices_groupby='grade', required=False
    # )  
    
    # topics = forms.ModelChoiceField(widget=forms.SelectMultiple, queryset=Topic.objects.filter(grade=2), required=False)
    
    class Meta:
        model = Question
        # fields = ('subject',  'question', 'question', 'option_A', 'option_B', 'option_C', 'option_D', 'answer','topics', )
        exclude = ("topics", "exam", 'updated', 'created')
        widgets = {
            'question': TinyMCE(attrs={"cols":80, "rows":30}),
        }
        
    def __init__(self,request,  *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.teacher = request.user
        # self.fields["question"].widget.attrs.update({"rows":5,}) 
        self.fields["question"].required = True
        # self.fields["topics"].empty_label = "Select topic"
        # self.fields['topics'].queryset = Topic.objects.filter(subject__teacher=request.user).order_by('grade')
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
    