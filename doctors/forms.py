from django import forms
from .models import Appointment
class myform(forms.Form):
    userQuery=forms.CharField(label='name',min_length=1)





class Appointmentform(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['P_name','P_age', 'state', 'dist', 'appoint_date', 'appoint_time']
