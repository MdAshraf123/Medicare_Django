from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user,'doctors'):
            return redirect('main:login')
        return view_func(request, *args, **kwargs)
    
    return wrapper

def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if not hasattr(request.user,'patients'):
            return HttpResponse('Unauthorized access')
        return view_func(request,*args,**kwargs)
    return wrapper