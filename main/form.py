from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from doctors.models import Doctors

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = None

class ProfileEditForm(forms.ModelForm):
    doctor_face = forms.ImageField(required=False)
    class Meta:
        model=Doctors
        fields=['name','degree','speciality','hospital','address','p_count','experience','map_location','about']
        widgets={
            # 'doctor_face':forms.ClearableFileInput(attrs={
            #     'placeholder':'Upload Your image.',
            #     'class':'doctor_face',
            #     'required':'False'
            # }), 
            'name':forms.TextInput(attrs={
                'placeholder':'Enter your name.',
            }),
            'degree':forms.TextInput(attrs={
                'placeholder':'Enter degree' ,
            }),
            'speciality':forms.TextInput(attrs={
                'placeholder':'Enter speciality',
            }),
            'hospital':forms.TextInput(attrs={
                'placeholder':'Enter hospital name',
            }),
            'address':forms.TextInput(attrs={
                'placeholder':'Enter address',
            }),
            'p_count':forms.NumberInput(attrs={
                'placeholder':'Enter your daily pateint limit',
                'inputmode':'numeric',
                'style': 'appearance: textfield; -moz-appearance: textfield;'
            }),
            'experience':forms.NumberInput(attrs={
                'placeholder':'Enter experience in year',
                'inputmode':'numeric',
                'style': 'appearance: textfield;' ,
            }),
            'map_location':forms.TextInput(attrs={
                'placeholder':"Embed your location from google map",
                
            })
            ,
            'about':forms.Textarea(attrs={
                'placeholder':'Write about you',
            })
        }
    def __init__(self, *args,**kwargs):
        super(ProfileEditForm,self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label =''
            self.fields[field_name].help_text = None