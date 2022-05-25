"""it_sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# CALLING URL NAME AND THE FUNCTION IN views.py

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('home',views.home,name='home'),
    path('copd', views.copd, name='copd'),
    path('copdresults', views.copdresults, name='copdresults'),
    path('diabetes', views.diabetes, name='diabetes'),
    path('heart', views.heart, name='heart'),
    path('logout',views.logout,name='logout'),
    path('accountUpdate',views.accountUpdate,name='accountUpdate'),
    path('forgotpass',views.forgotpass,name='forgotpass'),
    path('forgotpass2',views.forgotpass2,name='forgotpass2'),


]

urlpatterns += staticfiles_urlpatterns()