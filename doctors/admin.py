from django.contrib import admin
from .models import Doctor
# Register your models here.
class DocAdmin(admin.ModelAdmin):
    list_display=('id','name','degree','speciality','hospital','address','p_count')
admin.site.register(Doctor,DocAdmin)
