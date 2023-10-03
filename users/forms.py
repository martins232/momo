from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . models import User, Student
from django.contrib.auth.forms import UserCreationForm
from datetime import date # used in birthday validation
import datetime # used to prevent future date



role_choice = (
    ("student", "Student"),
    ("teacher", "Teacher")
)

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        label= "Select your role",
        required=True,
        choices=role_choice, 
        error_messages= {"required": "Please select a role"},
        widget=forms.RadioSelect(attrs={
            "class": "form-control"
        })
        )
    first_name = forms.CharField(
        label="First name",
        min_length=3,
        max_length=50,
        # required=False,
        validators=[RegexValidator(r"^[a-zA-Z]*$", message="Only letters are allowed")], 
        error_messages= {"required": "Firstname cannot be empty"},
        widget=forms.TextInput(attrs={
            "placeholder":"Enter First name",
            "style": "text-transform: capitalize;"            
            })
        ) 
    last_name = forms.CharField(
        label="Last name",
        min_length=3,
        max_length=50,
        # required=False,
        validators=[RegexValidator(r"^[a-zA-Z]*$", message="Only letters are allowed")], 
        error_messages= {"required": "Lastname cannot be empty"},
        widget=forms.TextInput(attrs={
            "placeholder":"Enter Last name",
            "style": "text-transform: capitalize;"            
            })
        ) 
    
    
    class Meta:
        
        model = User
        fields = ["first_name", "last_name","username", "role", "password1", "password2"]
        
        
        labels ={
            "password2":"Started",
        }
        
        widgets ={
            "username": forms.TextInput(attrs={"class": "form-control","autofocus": False,}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})


class StudentRequestForm(forms.ModelForm):
    image = forms.FileField(
        label="Your picture",        
        required= True,
        widget=forms.ClearableFileInput(
            attrs={
                "style": "font-size : 13px;",
                "class": "form-control",
                "accept": "image/png, image/jpeg"
            }
        )
    )
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ["user"]
        
        
        GENDER = (
            ("M","Male"),
            ("F","Female")
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
        
    def __init__(self, request, *args, **kwargs):
        self.request = request # Assign the request object to the form instance
        super().__init__(*args, **kwargs) # Call the parent class constructor    
        
    
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


    def clean_image(self):
        image = self.cleaned_data.get("image")
        ext = str(image).split(".")[-1]
        if image.size <= 2*1048576:
            try:
                new_name = (self.request.user.first_name+"_"+self.request.user.last_name+"."+ext).lower() 
            except KeyError:
                return image
            else:
                image.name = new_name
                return image
        else:
            raise forms.ValidationError("Max. Upload: 2MB")