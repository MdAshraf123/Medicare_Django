from django.contrib import admin
from main.models import Topdoc

# from doctors.models import Doctor

# Register your models here.
class TopdocAdmin(admin.ModelAdmin):
    list_display=('did','dname','ddegree','dhospital','daddress','dexprience','dspeciality')


admin.site.register(Topdoc,TopdocAdmin)
