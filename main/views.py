from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from main.models import Topdoc
from main.models import UserProfileImages,Patients
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .form import CustomUserCreationForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from doctors.models import Appointment,Doctors
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.templatetags.static import static
from utils.decorators import doctor_required,patient_required
from django.contrib import messages
from decouple import config
import base64
import requests
import json


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():     
            user = form.get_user()
            if hasattr(user,'patients'):
                login(request, user)
                return redirect('main:home')
            elif hasattr(user, 'doctors'):
                login(request, user)
                return redirect('main:doctor_dashboard')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form })

@login_required
# @patient_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:home')
    return render(request, 'registration/logout.html')




def homepage(request ):
    TopD=Topdoc.objects.all()
    return render(request,f'core/home.html',{'TopD':TopD,})

@login_required
@patient_required
def bookedAppointment(request):
    obj=Appointment.objects.filter(patient=request.user)
    # obj2=Appointment.Doctor.objects.filter(id=obj.d_id)
    context = {
        'appointData':obj,    
    }
    return render(request,'core/bookedAppoints.html',context)

@login_required
@require_http_methods(["POST"])
def profileImageUpload(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
        updateUpload(request,profile_image)
        return JsonResponse({'message': 'Profile image uploaded successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_http_methods(["POST"])
def saveProfileChages(request):
    if request.method=='POST':
        user1=User.objects.get(id=request.user.id)
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        loc=request.POST.get('location')
        patientUser, is_created =Patients.objects.get_or_create(patient=user1)
        patientUser.phone_number =phone
        patientUser.location=loc
        patientUser.save()

        if not email.endswith('@gmail.com'):
            return JsonResponse({'error':'invalid error domail'}, status=400)
        user1.email=email
        user1.first_name=first_name
        user1.last_name=last_name
        user1.save()
        return JsonResponse({'successful':'data sent successfully'},status=200)
    return JsonResponse({'error':'invalid request method'}, status=400)


def contactpage(request):
    return render(request,'core/contact.html')


def aboutpage(request):
    return render(request,'core/about.html')


def updateUpload(request,profile_image):
    my_token = config("GITHUB_TOKEN")
  # Replace with your GitHub personal access token
    REPO_NAME = "MdAshraf123/media_cdn"  # Repository name (e.g., owner/repo)
    BRANCH_NAME = "main"  # Target branch
    FOLDER_PATH = "profile_images"  # Path in the repository
    # LOCAL_IMAGE_PATH = profile_image#"img6.jpeg"  # Replace with the path to your image
    IMAGE_NAME = f"image{request.user.id}.jpeg"  # Name of the image file to upload
    
    temp_file_path=default_storage.save(f"temp/{profile_image.name}",ContentFile(profile_image.read()))
    # Read the image and encode it in Base64
    try:
        with open(temp_file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")
    finally:
        default_storage.delete(temp_file_path)
    # GitHub API URL for creating/updating files
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FOLDER_PATH}/{IMAGE_NAME}"

    # HTTP Headers
    headers = {
        "Authorization": f"Bearer {my_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    tempresponse=requests.get(url,headers)
    if tempresponse.status_code==200:
        sha=tempresponse.json()['sha']
        payload={
            "message":f"Updating image {IMAGE_NAME} for userId- {request.user.id}",
            "content":encoded_content,
            "branch":BRANCH_NAME,
            "sha":sha,
        }
    else:
        payload={
            "message":f"Uploading image {IMAGE_NAME} for userId- {request.user.id}",
            "content":encoded_content,
            "branch":BRANCH_NAME,
        }

    response = requests.put(url, json=payload, headers=headers)

    # Handle the Response
    if response.status_code == 201:
        print(f"Image '{IMAGE_NAME}' uploaded successfully to {FOLDER_PATH}!")
        currentUser=User.objects.get(id=request.user.id)    
        UserProfileImages.objects.create(user=currentUser, u_p_image=f"https://raw.githubusercontent.com/MdAshraf123/media_cdn/main/profile_images/{IMAGE_NAME}")
    elif response.status_code == 200:
        print(f"Image '{IMAGE_NAME}' updated successfully in {FOLDER_PATH}!")
    else:
        print(f"Failed to upload image: {response.status_code}")

@login_required
@patient_required
@require_http_methods('POST')       
def cancelAppoint(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            user=data.get('userid')
            appointId=data.get('appointmentId')
            obj=Appointment.objects.get(id=appointId)
            obj.delete()
            return JsonResponse({
                'status':'success',
                'message':f'Deleted Successfully\nAppointment id- {appointId}'
            },status=200)
        except Appointment.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message':'Appointment not found',
            },status=404)
        except Exception as e:
            return JsonResponse({
                "status":"error",
                "message": e,
            })
    return JsonResponse(
        {
            'status':'Bad request',
        },status=400
    )

@login_required
@doctor_required
def doctor_dashboard(request):
    doctor=request.user.doctors
    appointments=Appointment.objects.filter(doctor=request.user)
    context={
        'appointments':appointments,
        'doctor':doctor,
        }
    return render(request, 'doctors/doctor_dashboard.html',context)

@login_required
@doctor_required
def doc_profile(request):
    doctor=Doctors.objects.get(doctor=request.user)
    messages.success(request, 'Doctor Profile')
    return render(request, 'doctors/doctorprofile.html',{'doctor':doctor})

@login_required
@doctor_required
def editdoctorprofile(request):
    doctor=request.user.doctors
    if request.method=='POST':
        form=ProfileEditForm(request.POST, request.FILES, instance=doctor)      
        if form.is_valid():
            file=request.FILES.get('doctor_face')
            if file:
                image_url = upload_image_to_github(request,file)
                doctor.doctor_face = image_url
            form.save()
            return HttpResponse( 'Successfully updated')
    else:
        form=ProfileEditForm(instance=doctor)
    return render(request,'doctors/editProfile.html',{'form':form})


def upload_image_to_github(request,file):

    GITHUB_TOKEN = config("GITHUB_TOKEN")
    REPO = "MdAshraf123/media_cdn"
    BRANCH = 'main'
    IMAGE_NAME = f"image{request.user.id}.jpeg"
    IMAGE_FOLDER = "profile_images"
    filename = f"dimage{request.user.id}.jpeg"
    content = base64.b64encode(file.read()).decode('utf-8')
    api_url = f'https://api.github.com/repos/{REPO}/contents/{IMAGE_FOLDER}/{filename}'
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "message": f"Upload {filename}",
        "branch": BRANCH,
        "content": content
    }
    get_resp=requests.get(api_url,headers=headers)
    if get_resp.status_code==200:
        sha=get_resp.json()['sha']
        data['sha']=sha
    else:
        sha=None

    

    response = requests.put(api_url, json=data, headers=headers)
    
    if response.status_code in [201, 200]:
        return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{IMAGE_FOLDER}/{filename}"
    else:
        raise Exception("GitHub upload failed: " + response.text)
