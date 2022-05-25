
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.index1,name='index'),
    path('patientlogin',views.patientlogin,name='patientlogin'),
    path('patienthome',views.patienthome,name='patienthome'),
    path('viewrecords',views.viewrecords,name='viewrecords'),
    ]
