from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import Topdoc,CustomUser
from main.models import UserProfileImages
# from your_app_name.models import CustomUser

# from doctors.models import Doctor

# Register your models here.
class TopdocAdmin(admin.ModelAdmin):
    list_display=('did','dname','ddegree','dhospital','daddress','dexprience','dspeciality')


admin.site.register(Topdoc,TopdocAdmin)




@admin.register(CustomUser) # used in small and concise use
class CustomUserAdmin(admin.ModelAdmin):
   list_display=['phone_number','location']


class UserProfileImages1(admin.ModelAdmin):
    list_display=('user','u_p_image')

admin.site.register(UserProfileImages,UserProfileImages1)