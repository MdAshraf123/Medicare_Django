from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from main.models import Topdoc
from main.models import UserProfileImages,CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .form import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from doctors.models import Appointment
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.templatetags.static import static
from decouple import config
import base64
import requests



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
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form })

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:home')
    return render(request, 'registration/logout.html')




def homepage(request ):
    TopD=Topdoc.objects.all()
    return render(request,f'core/home.html',{'TopD':TopD,})

@login_required
def profile(request):
    obj=Appointment.objects.filter(userid=request.user.id)
    # obj2=Appointment.Doctor.objects.filter(id=obj.d_id)
    user = request.user  # Get the currently logged-in user
    context = {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'userid': user.id,
        'username': user.username,
        'password': '********' , # Display password in dotted format
        'gmail':user.email,
        'appointData':obj,
        
    }
    return render(request,'core/profile.html',context)

@login_required
@require_http_methods(["POST"])
def profileImageUpload(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
        print("++++File name: "+request.FILES['profile_image'])
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
        customUser, is_created =CustomUser.objects.get_or_create(user=user1)
        customUser.phone_number =phone
        customUser.location=loc
        customUser.save()

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

# def login(request):
#     fm=loginFor(request.POST)
#     return render(request,'login/loging.html',{'form':fm})

# def Authorize(request):
#     fm=loginFor(request.POST)

#     if fm.is_valid():
#         # return HttpResponseRedirect('/home/')
#         user=fm.cleaned_data['user']
#         password=fm.cleaned_data['password']
#         if  User.objects.filter(Uname=user).exists() and User.objects.filter(Upassword=password).exists():
#             return HttpResponseRedirect(f'/home/?name={user}')
#         else:
#             return HttpResponse('false credentials ')
#     else:
#         return HttpResponse('form is not valid')

    

def hospitalpage(request):
    return HttpResponse('<h1>this is hospital page</h1>')


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
        
   

