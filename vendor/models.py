from django.db import models
from admins.models import Category

# Create your models here.

class Vendor(models.Model):
    username = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    

    
