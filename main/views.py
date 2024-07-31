from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from main.models import Topdoc
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .form import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from doctors.models import Appointment


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
            print('user_Id',user.id)
            print(user.username,user.password)
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:home')
    return render(request, 'registration/logout.html')



@login_required
def homepage(request):
    TopD=Topdoc.objects.all()
    return render(request,f'core/home.html',{'TopD':TopD})
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
def contactpage(request):
    return render(request,'core/contact.html')

@login_required
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

    
@login_required
def hospitalpage(request):
    return HttpResponse('<h1>this is hospital page</h1>')


