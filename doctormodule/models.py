from django.db import models

# Create your models here.

class Doctor(models.Model):
    doc_id = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50,default="None")
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50,help_text="Minimum of 8 Characters")
    dept = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    hospital=models.CharField(max_length=20)

    def __str__(self):
        return self.doc_id+";"+self.name+";"+self.gender+";"+self.email+";"+self.password+";"+self.dept+";"+self.phone+";"+self.hospital


class Patients(models.Model):
    name = models.CharField(max_length=50)
    AID= models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50, default="None")

    type = models.CharField(max_length=50)
    stage = models.CharField(max_length=20)
    treatement=models.CharField(max_length=300)



    @staticmethod
    def validteuser(AID,email):
        print(AID,email)
        print(AID,email)
        try:
         contents=Patients.objects.get(AID=AID,email=email)
         print(contents.email)
         return 'yes'
        except Patients.DoesNotExist:
          return 0



