import email
from django import forms
from django.core.validators import RegexValidator
from teachers.models import Topic, Subject
from users  . models import User, Teacher
from  django.core.files.base import File



class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()
class UserUpdateForm(forms.ModelForm):
    
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
    first_name = forms.CharField(
    label="First name",
    help_text="<p>Space and numbers are not acceptable</p>",
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
        help_text="<p>Space and numbers are not acceptable</p>",
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
        fields = ["first_name", "last_name","username", "email"]
        
        widgets ={
                "username": forms.TextInput(attrs={"class": "form-control","autofocus": False,}),
            }    
    def __init__(self,request,*args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = "Use a verifiable email, should you want to reset your password"
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields["username"].error_messages.update({"unique": "Denied! User already exist. You may want to login?"})
        
        if request.user:
            if request.user.is_student is not None:
                # If yes, remove the role field
                self.fields.pop('email')
    
    def clean_username(self):
        """This is to make sure a user can updaate his/her **username** without getting an error"""
        username = self.cleaned_data.get('username')
        current_user = self.request.user

        if User.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError("Denied! User already exists. You may want to login?")

        return username  
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            if self.request.user.email == email:
                return email
            else:
                raise forms.ValidationError("Denied! " + email + " is already registered to another teacher")    
        return email
    



class TeacherUpdateForm(forms.ModelForm):
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
        exclude = ["user", "status", "image"]  
        
        GENDER = (
            ("Male","Male"),
            ("Female","Female")
        )
        
        widgets ={
            "phone" :forms.TextInput(
                attrs={
                    "type": "telephone",
                    "style": "font-size:14px; ", #CSS
                    "placeholder": "E.g: 07030000000",
                   
                }
            ),
             "gender":forms.RadioSelect(choices=GENDER, attrs={"class":"btn-check",}),
        }
    
    def __init__(self, request, *args, **kwargs):
        self.request = request # Assign the request object to the form instance
        super().__init__(*args, **kwargs) # Call the parent class constr
        self.fields["image"].required = False
        # self.helper = FormHelper()  I removed it because it wasn't showing validation again
        # self.helper.template_pack = 'bootstrap4' # Set the template pack
        # fields =('email', 'phone', 'gender', "image")
        # for field in fields:
        #     self.fields[field].label = ""
        
    # def clean_image(self):
    #     image = self.cleaned_data.get("image")
    #     if image.size <= 2*1048576:
    #         # try:
    #         #     new_name = (self.request.user.first_name+"_"+self.request.user.last_name+"."+ext).lower() 
    #         # except KeyError:
    #         #     return image
    #         # else:
    #         #     image.name = new_name
    #         return image
    #     else:
    #         raise forms.ValidationError("Max. Upload: 2MB")
    
       
        
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise forms.ValidationError("Invalid number")
        return phone
    
    
    
    
class ChangeProfilePicture(forms.ModelForm):
    image = forms.FileField(
        label="Your picture",   
        required=True,
        widget=forms.FileInput(
            attrs={
                "style": "font-size : 13px;",
                "class": "form-control",
                "accept": "image/png, image/jpeg",
            }
        )
    )
    class Meta:
        model = Teacher
        fields = ["image"]
        
        
    def clean_image(self):
        image = self.cleaned_data["image"]
        if isinstance(image.file, File): #to check if an image was uploaded
            raise forms.ValidationError("Please select an image")
        else:
            if image.size <= 2*1048576:
                return image
            else:
                raise forms.ValidationError("Max. Upload: 2MB")
            
            
class TopicForm(forms.ModelForm):
    
    class Meta:
        model= Topic
        fields = "__all__"
        
    def __init__(self, request, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(teacher=request.user)
        self.fields['name'].label = "Topic name"
        
