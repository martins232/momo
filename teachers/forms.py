from django import forms
from django.core.validators import RegexValidator
from users  . models import User, Teacher
from crispy_forms.helper import FormHelper




class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()

class TeacherUpdateForm(forms.ModelForm):
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
        fields =('email', 'phone', 'gender', "image")
        for field in fields:
            self.fields[field].label = ""
        
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image.size <= 2*1048576:
            # try:
            #     new_name = (self.request.user.first_name+"_"+self.request.user.last_name+"."+ext).lower() 
            # except KeyError:
            #     return image
            # else:
            #     image.name = new_name
            return image
        else:
            raise forms.ValidationError("Max. Upload: 2MB")
    
       
        
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise forms.ValidationError("Incomplete number: 08100124724")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Teacher.objects.filter(email=email).exists():
            if self.request.user.teacher.email == email:
                return email
            else:
                raise forms.ValidationError("Denied! " + email + " is already registered to another teacher")    
        return email