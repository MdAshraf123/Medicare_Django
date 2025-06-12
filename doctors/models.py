from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.
class Doctors(models.Model): 
    doctor=models.OneToOneField(User,on_delete=models.CASCADE, related_name='doctors',null=True, blank=True)
    doctor_face=models.URLField(default='NotUploaded')
    name=models.CharField(max_length=20)
    degree=models.CharField(max_length=15)
    speciality=models.CharField(max_length=25)
    about=models.CharField(max_length=175,default='Nothing')
    hospital=models.CharField(max_length=25)
    address=models.CharField(max_length=50)
    map_location=models.CharField(max_length=320, default='Empty')
    p_count=models.IntegerField(default=0)
    experience=models.IntegerField(validators=[MaxValueValidator(80), MinValueValidator(0)], default=0)
    rating=models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(0)],default=0)
    

    def __str__(self):
        return f"{self.name},{self.speciality}"
    

class DoctorLeave(models.Manager):
    L_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date=models.DateTimeField(default='Empty')
    duration=models.IntegerField(validators=[MaxValueValidator(15),MinValueValidator(1)])
    is_completed=models.BooleanField(default=False)

    
class Appointment(models.Model):
    class Gender(models.TextChoices):
        MALE='M','Male'
        FEMALE='F','Female'
        OTHER='O','Other'

   
    patient=models.ForeignKey(User, on_delete=models.CASCADE,  related_name='patient_appointments', null=True)
    doctor=models.ForeignKey(User, on_delete=models.CASCADE,  related_name='doctor_appointments',null=True)
    P_name=models.CharField(max_length=30)
    P_age=models.IntegerField(default=0)
    P_sex=models.CharField(max_length=2, choices=Gender.choices , default=Gender.MALE)
    P_contact=models.CharField(max_length=10, default='1234567890',validators=[RegexValidator(r"^\d{10}$","Enter 10 digit phone no.")])
    state=models.CharField(max_length=25)
    dist=models.CharField(max_length=25)
    appoint_date=models.DateField()
    appoint_time=models.TimeField(null=True, blank=True)
    is_complete=models.BooleanField(default=False)
    rateus= models.FloatField(default=0)#should add here a rating field
    
    
    def __str__(self):
        return f'{self.patient},{self.doctor},{self.P_name}'

