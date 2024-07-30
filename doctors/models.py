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