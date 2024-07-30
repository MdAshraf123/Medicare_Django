from django.db import models

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
    
# class User(models.Model):
#     Uname=models.CharField(max_length=15)
#     Upassword=models.CharField(max_length=10)
#     def __str__(self):
#         return f'{self.Uname},{self.Upassword}'
