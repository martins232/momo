from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . models import User
from django.contrib.auth.forms import UserCreationForm

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
        label="First name",
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



