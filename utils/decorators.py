from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user,'doctors'):
            return HttpResponse("unauthorized user")
        return view_func(request, *args, **kwargs)
    
    return wrapper