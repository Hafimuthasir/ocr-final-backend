from django.db import models

# Create your models here.

class UserInfo(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    phone = models.CharField(max_length=12)
    Country = models.CharField(max_length=100)
    id_type = models.CharField(max_length=100)
    id_proof = models.FileField(upload_to='./idproof')

class id_data(models.Model):
    userid = models.OneToOneField(UserInfo,on_delete = models.CASCADE)
    id_no = models.CharField(max_length=100,blank=True,null=True)
    id_name = models.CharField(max_length=100,blank=True,null=True)
    id_dob = models.CharField(max_length=50,blank=True,null=True)
    id_fulldata = models.TextField(blank=True,null=True)
    id_type = models.CharField(max_length=100)

