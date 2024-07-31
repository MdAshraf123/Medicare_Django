from django import forms
from .models import Appointment
class myform(forms.Form):
    userQuery=forms.CharField(label='name',min_length=1)





class Appointmentform(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['P_name','P_age', 'state', 'dist', 'appoint_date', 'appoint_time']
        widgets = {
            'P_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control'
            }),
            'P_age': forms.NumberInput(attrs={
                'placeholder': 'Enter your age',
                'class': 'form-control'
            }),
            'state': forms.TextInput(attrs={
                'placeholder': 'Enter your state',
                'class': 'form-control'
            }),
            'dist': forms.TextInput(attrs={
                'placeholder': 'Enter your district',
                'class': 'form-control'
            }),
            'appoint_date': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control'
            }),
            'appoint_time': forms.TimeInput(attrs={
                'placeholder': 'HH:MM',
                'class': 'form-control'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(Appointmentform, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ""