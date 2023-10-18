from users.models import Student
from django import forms
from datetime import date

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

