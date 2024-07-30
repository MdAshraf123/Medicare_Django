from django import forms
class myform(forms.Form):
    userQuery=forms.CharField(label='name',min_length=1)


class Appointmentform(forms.Form):
    patient_name=forms.CharField(max_length=30)
    patient_state=forms.CharField(max_length=13)
    patient_dist=forms.CharField(max_length=20)
    appoint_date=forms.DateField()
    appoint_time=forms.TimeField()
