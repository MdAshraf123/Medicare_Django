from django.urls import path
from . import views
urlpatterns=[
    path('doctors/',views.dmainpage,name='doctors'),
    path('Search/',views.searchBar,name='searching'),
    path('response/<str:speciality>/',views.response, name='filterView'),
    path('<int:idd>/appointmentForm/',views.appointform,name='appointform'),
    path('create_order/', views.create_order, name='create_order'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
]