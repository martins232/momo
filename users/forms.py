from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . models import User, Student, Teacher, Grade
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from datetime import date # used in birthday validation
# import datetime # used to prevent future date

# import unicodedata



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
        help_text="<p>Space and numbers are not acceptable</p>",
        min_length=3,
        max_length=50,
        # required=False,
        validators=[RegexValidator(r"^[a-zA-Z]*$", message="Only letters and numbers are allowed")], 
        error_messages= {"required": "Firstname cannot be empty"},
        widget=forms.TextInput(attrs={
            "placeholder":"Enter First name",
            "style": "text-transform: capitalize;"            
            })
        ) 
    last_name = forms.CharField(
        label="Last name",
        help_text="<p>Space and numbers are not acceptable</p>",
        min_length=3,
        max_length=50,
        # required=False,
        validators=[RegexValidator(r"^[a-zA-Z]*$", message="Only letters and numbers are allowed")], 
        error_messages= {"required": "Lastname cannot be empty"},
        widget=forms.TextInput(attrs={
            "placeholder":"Enter Last name",
            "style": "text-transform: capitalize;"            
            })
        ) 
    
    
    
    class Meta:
        
        model = User
        fields = ["first_name", "last_name","username", "role", "password1", "password2"]
        
        
        widgets ={
            "username": forms.TextInput(attrs={"class": "form-control","autofocus": False,}),
            
        }

    
    def __init__(self,request,*args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields["username"].error_messages.update({"unique": "Denied! User already exist. You may want to login?"})
        
        if request.user:
            if request.user.pk:
                # If yes, remove the role field
                self.fields.pop('role')
                
                
    def clean_username(self):
        """This is to make sure a user can updaate his/her **username** without getting an error"""
        username = self.cleaned_data.get('username')
        current_user = self.request.user

        if User.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError("Denied! User already exists. You may want to login?")

        return username    
    
    # def clean(self):
    #     # call the parent class's clean method
    #     cleaned_data = super().clean()
    #     # get the values from the cleaned_data dictionary
    #     role = cleaned_data.get("role")
    #     username = cleaned_data.get("username")
    #     # check if the user already exists and wants to update their profile
    #     if self.request.user and self.request.user.pk:
    #         # remove the role field from the cleaned_data
    #         cleaned_data.pop("role")
    #     else:
    #         # check if the role field is empty
    #         if not role:
    #             # raise a validation error
    #             raise forms.ValidationError("Please select a role")
    #     # check if the username field is unique
    #     if User.objects.filter(username=username).exists():
    #         # raise a validation error
    #         raise forms.ValidationError("Denied! User already exist. You may want to login?")
    #     # return the cleaned_data dictionary
    #     return cleaned_data
    
    
    # # def clean_email(self, request):
    # #     username = self.cleaned_data.get("username")
    # #     if User.objects.filter(username=username).exists():
    # #         if request.user.username == username:
    # #             return username
    # #         else:
    # #             raise forms.ValidationError("Denied! " + username + " is already registered")
    # #     return username

class StudentRequestForm(forms.ModelForm):
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
    
    
    image = forms.FileField(
        label="Your picture",     
        required= False, # bring out the checkbox
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
        # fields = "__all__"
        exclude = ["status","user", "request_password"]
        
        
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
        
    def __init__(self, request, *args, **kwargs):
        self.request = request # Assign the request object to the form instance
        super().__init__(*args, **kwargs) # Call the parent class constructor    
        # if request.user:
        #     if request.user.pk:
        #         # If yes, remove the role field
        #         # self.fields["gender"].disabled=True
        #         pass
        
    
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
        if age<10 or age >65:
            raise forms.ValidationError("Age must be between 10 and 65")
        
        return birth
    # def clean_image(self):
    #     image = self.cleaned_data.get("image")
    #     if image.size <= 2*1048576:
    #         return image
    #     else:
    #         raise forms.ValidationError("Max. Upload: 2MB")

    def clean_image(self):
        image = self.cleaned_data.get("image")
        
        
        if image is not None:
            if image.size <= 2*1048576:
                return image
            else:
                raise forms.ValidationError("Max. Upload: 2MB")
        else:
            pass
            # raise forms.ValidationError("Image is required")
        
        
class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()
    
class TeacherRequestForm(forms.ModelForm):
    email = LowerCase(
        label="Email",
        min_length=10,
        max_length=50,
        # required=False,
        validators=[RegexValidator(r"^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9.+-_]+\.[a-zA-Z]*$", message="Enter a valid email address")], 
        widget=forms.TextInput(attrs={
            "placeholder":"Email Address",
            "style": "font-size : 13px; text-transform: lowercase;",
            # "autocomplete": "off" -----already done in supr func
            }
        )
    )
    
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
        model = Teacher
        exclude = ["user", "status"]  
        
        GENDER = (
            ("Male","Male"),
            ("Female","Female")
        )
        
        widgets ={
            "phone" :forms.TextInput(
                attrs={
                    "style": "font-size:14px; ", #CSS
                    "placeholder": "E.g: 0703-0000-000",
                    
                }
            ),
             "gender":forms.RadioSelect(choices=GENDER, attrs={"class":"btn-check",}),
        }
    
    def __init__(self, request, *args, **kwargs):
        self.request = request # Assign the request object to the form instance
        super().__init__(*args, **kwargs) # Call the parent class constr
        # if request.user:
        #     if request.user.pk:
        #         # self.fields["gender"].disabled=True
        #         self.fields.pop("email")
    def clean_image(self):
        image = self.cleaned_data.get("image")
        
        
        if image.size <= 2*1048576:
            return image
        else:
            raise forms.ValidationError("Max. Upload: 2MB")
       
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise forms.ValidationError("Invalid number")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            if email == self.request.user.email:
                return email
            else:
                raise forms.ValidationError("Denied! " + email + " is already registered")
        return email
    

# def _unicode_ci_compare(s1, s2):
#     """
#     Perform case-insensitive comparison of two identifiers, using the
#     recommended algorithm from Unicode Technical Report 36, section
#     2.11.2(B)(2).
#     """
#     return (
#         unicodedata.normalize("NFKC", s1).casefold()
#         == unicodedata.normalize("NFKC", s2).casefold()
#     )
# class CustomPasswordResetForm(PasswordResetForm):
#     def get_users(self, email):
#         """
#         Retrieve users based on the provided email address.
#         Override this method to handle unusable passwords.
#         """
#         active_users = Teacher.objects.filter(
#             **{
#                 "%s__iexact" % "email": email,
#                 "user__is_active": True,
#             }
#         )
#         print(active_users)
#         return (
#             u
#             for u in active_users
#             if u.user.has_usable_password()
#             and _unicode_ci_compare(email, getattr(u, "email"))
#         )
        
    