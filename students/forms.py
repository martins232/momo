from urllib import request
from users.models import Student, User
from django import forms
from datetime import date
from django.contrib.auth.forms import PasswordChangeForm


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ["user", "status", "image"]
        
        
        GENDER = (
            ("Male","Male"),
            ("Female","Female")
        )
        
        widgets ={
            # Birth date
            "birth": forms.DateInput(
                attrs={
                     "style": "font-size:14px; cursor:pointer",
                     "type":"date",
                     "onkeydown":"return True", # Javascript prevent typing
                     "min":"1958-01-01",
                     "max": "2011-12-31"
                }
            ),
            "gender":forms.RadioSelect(choices=GENDER, attrs={"class":"btn-check",}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["grade"].disabled = True
        
    def clean_birth(self):
        birth = self.cleaned_data.get("birth")
        # variables
        b = birth
        now = date.today()
        age = (now.year - b.year) - ((now.month, now.day) < (b.month, b.day))
        """ 
        age = (now.year - b.year) - ((now.month, now.day) < (b.month, b.day)) # i.e. 27 - ((9, 29) < (10, 26))
            ((now.month, now.day) < (b.month, b.day)) == ((9, 29) < (10, 26))
            Your answer will be True because (9, 29) is less than (10, 26) since 9(september) is less than 10(october) you haven't clocked 27 yet. The second elements of the tuples are not compared at all, as the first elements are enough to decide the result. You can think of it as comparing words in a dictionary: "apple" comes before "banana" because "a" comes before "b", regardless of the rest of the letters.
            Therefore (27 - True) is thesame as 27 -1 = 26
        """
        if age<18 or age >65:
            raise forms.ValidationError("Age must be between 18 and 65")
        
        return birth

class studentPasswordReset(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        fields = ["old_password", "new_password1", "new_password2"]
        for field in fields:
            self.fields[field].widget.attrs.update({'autofocus': False, "style": "font-size:14px;" })
            
        self.fields["old_password"].help_text = "You are to input your old password"
    
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        current_user = self.user
       
        if current_user.check_password(old_password):
            return old_password
        else:
            raise forms.ValidationError("Old password doesn't match with what is in the database")