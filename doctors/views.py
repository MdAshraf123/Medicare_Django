from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .forms import myform,Appointmentform
from .models import Doctors,Appointment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from utils.decorators import doctor_required,patient_required
import json
from razorpay import Client  # Make sure you imported this
import razorpay
from django.conf import settings

# Create your views here.
def dmainpage(request):
    doctors = Doctors.objects.all()
    return render(request,'core/dhome.html',context={'data':doctors})

def response(request,speciality):
    D={ 
        'All':'*',
        'Ped':'Pediatrician',
        'Car':'Cardiologist',
        'Der':'Dermatologist',
        'Gas':'Gastroenterologist',
        'Hem':'Hematologist',
        'ENT':'ENT',
        'Den':'Dentist',
    }
    if D[speciality]=='*':
        doctors=Doctors.objects.all()
    else:
        doctors = Doctors.objects.filter(speciality=D[speciality])
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
                doctors = Doctors.objects.filter(name__startswith =valu)
            else:
                doctors=None
    else:
        form1=myform()

    return render(request,'core/dhome.html',context={'data':doctors})

@login_required
@patient_required
def appointform(request,idd):
    if request.method=='POST':
        # form = Appointmentform(request.POST)
        # doctorId=Doctor.objects.get(id=idd)
        # if form.is_valid():

        #     appointment = form.save(commit=False)
        #     appointment.d_id = doctorId
        #     appointment.userid=request.user.id
        #     appointment.save()
            return HttpResponse('booking successfull')
    else:
        appointForm=Appointmentform()
        return render(request,'core/appointForm.html',{'form':appointForm,'id':idd})
    




# Initialize Razorpay client
client = razorpay.Client(auth=( settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRETE))
@login_required
@patient_required
@csrf_exempt
def create_order(request):
    if request.method == "POST":
        # You can calculate the amount dynamically based on your form input
        amount = 10000  # Example: 500.00 INR = 50000 paise
        # Create Razorpay order
        order = client.order.create(dict(amount=amount, currency="INR", payment_capture="1"))
        
        # Order ID returned from Razorpay
        order_id = order['id']

        # Return order ID to frontend
        return JsonResponse({'order_id': order_id})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@patient_required
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        payment_data = request.POST.dict() 
        if not payment_data:
            payment_verification= json.loads(request.body) # Extract payment response from frontend
            payment_data= payment_verification.get("paymentResponse")
            appoint_data= payment_verification.get("formData")
        # Verify payment signature
        try:
            client.utility.verify_payment_signature(payment_data)
            # If the signature is verified, mark the payment as successful
            order_id = payment_data.get("razorpay_order_id")
            payment_id = payment_data.get("razorpay_payment_id")
            appointmentForm= Appointmentform(appoint_data)

            if appointmentForm.is_valid():
                obj=appointmentForm.save(commit=False)
                obj.patient=request.user
                obj.doctor= Doctors.objects.get(id= appoint_data.get('doctor')).doctor
                obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})