from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Doctor(models.Model): 
    duser=models.CharField(max_length=10, default='1234')
    dpass=models.CharField(max_length=15, default='123456')
    doctor_face=models.URLField(default='Empty')
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
    raters_number=models.IntegerField(default=0)#should be deleted
    

    def __str__(self):
        return f"{self.name},{self.speciality}"
    

class DoctorLeave(models.Manager):
    L_id=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    date=models.DateTimeField(default='Empty')
    duration=models.IntegerField(validators=[MaxValueValidator(15),MinValueValidator(1)])
    is_completed=models.BooleanField(default=False)

    
class Appointment(models.Model):
    class Gender(models.TextChoices):
        MALE='M','Male'
        FEMALE='F','Female'
        OTHER='O','Other'

   
    userid=models.ForeignKey(User, on_delete=models.CASCADE)
    d_id=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    P_name=models.CharField(max_length=30)
    P_age=models.IntegerField(default=0)
    P_sex=models.CharField(max_length=2, choices=Gender.choices , default=Gender.MALE)
    P_contact=models.CharField(max_length=10, default='1234567890')
    state=models.CharField(max_length=25)
    dist=models.CharField(max_length=25)
    appoint_date=models.DateField()
    appoint_time=models.TimeField(null=True, blank=True)
    is_complete=models.BooleanField(default=False)
    rateus= models.FloatField(default=0)#should add here a rating field
    
    
    def __str__(self):
        return f'{self.userid},{self.d_id},{self.P_name}'

