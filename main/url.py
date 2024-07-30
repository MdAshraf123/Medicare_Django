from django.urls import path,include
from main import views
from django.contrib.auth import views as auth_views
app_name='main'
urlpatterns=[ 
    path('home/',views.homepage,name='home'),
    # path('doctors/', views.doctorpage,name='doctors'),
    path('hospitals/',views.hospitalpage,name='hospitals'),
    path('contact/',views.contactpage,name='contact'),
    path('about/',views.aboutpage,name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile,name='profile'),
     
]