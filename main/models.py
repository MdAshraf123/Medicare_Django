from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Topdoc(models.Model):
    did=models.IntegerField(primary_key=True)
    dname=models.CharField(max_length=15)
    ddegree=models.CharField(max_length=10)
    dhospital=models.CharField(max_length=20)
    daddress=models.CharField(max_length=30)
    dexprience=models.CharField(max_length=10)
    dspeciality=models.CharField(max_length=20)
    dimage=models.URLField(default='no image')

    def __str__(self):
        return f'{self.did},{self.dname}'
    

class Patients(models.Model):
    patient=models.OneToOneField(User,on_delete=models.CASCADE, related_name='patients')
    phone_number =models.CharField(max_length=15,
                                   validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number')],
                                    null=False, blank=True) 
    
    location=models.CharField(max_length=50, null=False, blank=True)

    def isProfileComplete(self):
        return bool(self.patient and self.phone_number and self.location)
    

    def __str__(self):
        return f'{self.phone_number} {self.location}'
   
    

class UserProfileImages(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='patientsImgs')
    u_p_image=models.URLField(default='NotUploaded')

    def __str__(self):
        return f'{self.u_p_image}'
