from django.shortcuts import render
from django.http import HttpResponse
from .forms import myform,Appointmentform
from .models import Doctor,Appointment


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


def appointform(request,id):
    if request.method=='POST':
        print('this is doctor id',id)
        form = Appointmentform(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.id = id
            appointment.userid=request.user.id
            appointment.save()
            return HttpResponse('booking successfull')
    else:
        appointForm=Appointmentform()
        print('this is req obj',request)
        return render(request,'core/appointForm.html',{'form':appointForm,'id':request.user.id})