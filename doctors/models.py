from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Doctor(models.Model):
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
    raters_number=models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.name},{self.speciality}"
    

class DoctorLeave(models.Manager):
    L_id=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    date=models.DateTimeField(default='Empty')
    duration=models.IntegerField(validators=[MaxValueValidator(15),MinValueValidator(0)])
    is_completed=models.BooleanField(default=False)

    
class Appointment(models.Model):
    class Gender(models.TextChoices):
        MALE='M','Male'
        FEMALE='F','Female'
        OTHER='O','Other'

   
    userid=models.IntegerField(null=True)
    d_id=models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    P_name=models.CharField(max_length=30)
    P_age=models.IntegerField(default=0)
    P_sex=models.CharField(max_length=2, choices=Gender.choices , default=Gender.MALE)
    state=models.CharField(max_length=25)
    dist=models.CharField(max_length=25)
    appoint_date=models.DateField()
    appoint_time=models.TimeField(blank=True)
    is_complete=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.userid},{self.d_id},{self.P_name}'

