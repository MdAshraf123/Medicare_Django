from django.shortcuts import render
from django.http import HttpResponse
from .forms import myform
from .models import Doctor


# Create your views here.
def dmainpage(request):
    doctors = Doctor.objects.all()
    return render(request,'core/dhome.html',context={'data':doctors})

def response(request,speciality):
    D={ 'Ped':'Pediatrician',
        'Car':'Cardiologist',
        'Der':'Dermatologist',
        'Gas':'Gastroenterologist',
        'Hem':'Hematologist',
        'ENT':'ENT',
        'Den':'Dentist',
    }
    doctors = Doctor.objects.filter(speciality=D[speciality])
    return render(request,'core/dhome.html',{'data':doctors})

def searchBar(request):
    valu=0 
    if request.method=='POST':
        form1=myform(request.POST)
        if form1.is_valid():
            # valu=request.POST.get('userQuery')
            doctors=None
            valu=form1.cleaned_data['userQuery']
            if valu!='':
                doctors = Doctor.objects.filter(name__startswith =valu)
            else:
                doctors=None
    else:
        form1=myform()

    return render(request,'core/dhome.html',context={'data':doctors})
