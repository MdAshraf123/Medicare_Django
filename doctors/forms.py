from django import forms
from .models import Appointment
from datetime import datetime, timedelta
class myform(forms.Form):
    userQuery=forms.CharField(label='name',min_length=1)





# class Appointmentform(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['P_name','P_age','P_sex', 'state', 'dist', 'appoint_date']
#         widgets = {
#             'P_name': forms.TextInput(attrs={
#                 'placeholder': 'Enter your name',
#                 'class': 'form-control'
                
#             }),
#             'P_age': forms.NumberInput(attrs={
#                 'placeholder': 'Enter your age',
#                 'class': 'form-control'
#             }),
#             'P_sex':forms.RadioSelect(attrs={
#                 'class':'form-control'
#             }),
#             'state': forms.TextInput(attrs={
#                 'placeholder': 'Enter your state',
#                 'class': 'form-control'
#             }),
#             'dist': forms.TextInput(attrs={
#                 'placeholder': 'Enter your district',
#                 'class': 'form-control'
#             }),
#             'appoint_date': forms.Select(attrs={
#                 'class': 'form-control',
#                 'type':'date'
#             }),
           
#         }
#     def __init__(self, *args, **kwargs):
#         super(Appointmentform, self).__init__(*args, **kwargs)
#         for field_name in self.fields:
#             self.fields[field_name].label = ""
            
#         self.fields['appoint_date'].choices=[
#             ('', 'Select a date'), #placeholder options
#             ('20/2/2004','20/2/2004'),
#             ('3/6/2019','3/6/2019'),
#             ('4/9/2000','3/6/2019'),
#         ]
    

class Appointmentform(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['P_name', 'P_age', 'P_sex', 'state', 'dist', 'appoint_date',]
        widgets = {
            'P_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'p-name'
            }),
            'P_age': forms.NumberInput(attrs={
                'placeholder': 'Enter your age',
                'class': 'p-age'
            }),
            'P_sex': forms.RadioSelect(attrs={
                'class': 'p-sex'
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
                'class': 'form-control',
                'type':'date',
            }),
            
        }

    def __init__(self, *args, **kwargs):
        super(Appointmentform, self).__init__(*args, **kwargs)
        # Setting choices for the appoint_date dropdown

        today = datetime.today()

        # Calculate the date 3 days from today
        max_date = today + timedelta(days=3)

        # Format both dates in the proper format (YYYY-MM-DD)
        min_date = today.strftime('%Y-%m-%d')
        max_date = max_date.strftime('%Y-%m-%d')

        # Set the min and max values for the appoint_date field
        self.fields['appoint_date'].widget.attrs['min'] = min_date
        self.fields['appoint_date'].widget.attrs['max'] = max_date

       
        # for field_name in self.fields:
        #     self.fields[field_name].label = ""
