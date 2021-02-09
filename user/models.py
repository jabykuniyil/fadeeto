from django.db import models
from django.contrib.auth.models import User
from admins.models import Facilities, Category

# Create your models here.


class userData(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.BigIntegerField( null=True, blank=True)
    
     
    
    
# class Facilities(models.Model):
#     bath = models.BooleanField( null=True, blank=True)
#     purifiedWater = models.BooleanField( null=True, blank=True)
#     washRoom = models.BooleanField( null=True, blank=True)
#     shower = models.BooleanField( null=True, blank=True)
#     parking = models.BooleanField( null=True, blank=True)
#     gallery = models.BooleanField( null=True, blank=True)
#     cafteria = models.BooleanField( null=True, blank=True)
#     liveScreening  = models.BooleanField( null=True, blank=True)
#     locker = models.BooleanField( null=True, blank=True)
#     mobileCharging = models.BooleanField( null=True, blank=True)
    
    
    
class Turf(models.Model):
    sport = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    facilities = models.ForeignKey(Facilities, on_delete=models.CASCADE, null=True, blank=True)
    userDetails = models.ForeignKey(userData, on_delete=models.CASCADE, null=True, blank=True)
    turfName = models.TextField(  null=True, blank=True)
    timePeriod = models.TextField( null=True, blank=True)
    image1 = models.ImageField( null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    review = models.ImageField( null=True, blank=True)
    price = models.IntegerField( null=True, blank=True)
    mapImage = models.ImageField( null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    address = models.TextField( null=True, blank=True)
    
    
    @property
    def ImageURL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    
    @property
    def ImageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ""
        return url
    
class Booking(models.Model):
    userdata = models.ForeignKey(userData, on_delete=models.CASCADE, null=True, blank=True)    
    payment_option = models.CharField(max_length = 100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time_period = models.TextField( null=True, blank=True)
    sport = models.TextField(null=True, blank=True)
    turf_name = models.TextField(null=True, blank=True)