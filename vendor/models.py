from django.db import models
# from user.models import Turf
from admins.models import Category

# Create your models here.

class Vendor(models.Model):
    username = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    
# class vendorTurf(models.Model):
#     turfDetails = models.ForeignKey(Turf, on_delete = models.CASCADE)
#     turfName = models.CharField(max_length=20, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
    
    
# class turfObjectives(models.Model):
#     sport = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
