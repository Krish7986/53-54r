from django.db import models
class studentsNew(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField(null=True,blank=True)
    email=models.EmailField(unique=True)

class Users(models.Model):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
# Create your models here.
