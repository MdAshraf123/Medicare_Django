from main.models import UserProfileImages,CustomUser
from django.templatetags.static import static
from django.contrib.auth.models import AnonymousUser

def base_context(request):
    try:
        if request.user.is_authenticated:
            profileImageURL=UserProfileImages.objects.get(user=request.user)
            context={
                    'user':request.user,
                    'profileImageURL':profileImageURL.u_p_image,    
                }
        else:
            context={
                    'user':None,
                    'profileImageURL':static('images/user.png'),    
                }
    except UserProfileImages.DoesNotExist :
        context={
            'user':request.user,
            'profileImageURL':static('images/user.png'),
        }
    return context

def profileCompData(request):
    try:
        if request.user.is_authenticated:
            customUser=CustomUser.objects.get(user=request.user)
            print(customUser)
            context1={
                'isProfileComplete':customUser.isProfileComplete(),
                'profileRemainigData':{'phone':customUser.phone_number, 'location':customUser.location,},
            }
        else:
            context1={
                'isProfileComplete':None,
                'profileRemainigData':{'phone':None, 'location':None,},
            }
    except CustomUser.DoesNotExist:
        context1={
            'isProfileComplete':False,
            'profileRemainigData':{'phone':None, 'location':None,},
        }
    return context1
    