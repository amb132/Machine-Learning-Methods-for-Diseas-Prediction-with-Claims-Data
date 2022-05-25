from django.shortcuts import render,redirect
from doctormodule.models import Patients
# Create your views here.



def index1(request):

    return render(request,'Patients/index.html')



def patientlogin(request):
    global loginFlag, loginUser
    if request.method == 'POST':
        AID = request.POST['AID']
        email = request.POST['email']

        print(AID, email)
        message = ""

        if len(Patients.objects.filter(AID=AID)) == 0:
            message = message + "No Matching Accounts Found"
        else:
            patientdetails = Patients.objects.get(AID=AID)
            print(patientdetails.email)
            print(message)
            context = {"patientdetails": patientdetails}
            return render(request, 'Patients/Phome.html', context)




    else:
        return render(request, 'Patients/index.html')

def patienthome(request):

    return render(request, 'Patients/Phome.html')





def viewrecords(request):

    return render(request, 'Patients/Patientrecords.html')







