from django.contrib import admin

# Register your models here.
from .models import  Patients
from .models import Doctor

admin.site.register(Patients)
admin.site.register(Doctor)