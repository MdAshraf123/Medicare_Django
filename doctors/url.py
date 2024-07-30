from django.urls import path
from . import views
urlpatterns=[
    path('doctors/',views.dmainpage,name='doctors'),
    path('Search/',views.searchBar,name='searching'),
    path('response/<str:speciality>/',views.response, name='filterView'),
    path('<int:id>/appointmentForm/',views.appointform,name='appointform'),
]