from django.db import models

# Create your models here.
class Doctor(models.Model):
    name=models.CharField(max_length=20)
    degree=models.CharField(max_length=15)
    speciality=models.CharField(max_length=25)
    hospital=models.CharField(max_length=25)
    address=models.CharField(max_length=50)
    p_count=models.IntegerField()

    def __str__(self):
        return f"{self.name},{self.speciality}"
    
class Appointment(models.Model):
    userid=models.IntegerField(null=True)
    d_id=models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    P_name=models.CharField(max_length=30)
    P_age=models.IntegerField()
    state=models.CharField(max_length=25)
    dist=models.CharField(max_length=25)
    appoint_date=models.DateField()
    appoint_time=models.TimeField()
    def __str__(self):
        return f'{self.userid},{self.d_id},{self.P_name}'

