from django.contrib import admin
from .models import Doctor,Appointment
# Register your models here.
class DocAdmin(admin.ModelAdmin): 
    list_display=('id','name','degree','speciality','hospital','address','p_count','rating') 

class Appointment1(admin.ModelAdmin):
    list_display=('userid','d_id','P_name','P_age','state','dist','appoint_date','appoint_time')
admin.site.register(Doctor,DocAdmin)
admin.site.register(Appointment,Appointment1)

