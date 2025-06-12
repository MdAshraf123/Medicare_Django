from django.contrib import admin
from .models import Doctors,Appointment
# Register your models here.
class DocAdmin(admin.ModelAdmin): 
    list_display=('id','doctor','name','degree','speciality','hospital','address','p_count','rating') 

class Appointment1(admin.ModelAdmin):
    list_display=('id','patient','doctor','P_name','P_age','state','dist','appoint_date','appoint_time')
admin.site.register(Doctors,DocAdmin)
admin.site.register(Appointment,Appointment1)

