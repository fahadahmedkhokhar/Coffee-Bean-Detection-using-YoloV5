from django.db import models

# Create your models here.
class Account(models.Model):
    uname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    psw = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)