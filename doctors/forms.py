from django import forms
class myform(forms.Form):
    userQuery=forms.CharField(label='name',min_length=1)