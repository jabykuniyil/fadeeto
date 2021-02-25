from django.db import models
from django.contrib.auth.models import User
from admins.models import Facilities, Category
from vendor.models import Vendor

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=2500, null=True, blank=True)

class userData(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.BigIntegerField( null=True, blank=True)
    photo = models.ImageField(null=True, blank= True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    @property
    def ProfileURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
            
            
class Turf(models.Model):
    # sport = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    facilities = models.ForeignKey(Facilities, on_delete=models.CASCADE, null=True, blank=True)
    userDetails = models.ForeignKey(userData, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    turfName = models.TextField(null=True, blank=True)
    timePeriod = models.TextField( null=True, blank=True)
    image1 = models.ImageField( null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    mapImage = models.ImageField( null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    latitude = models.BigIntegerField(null=True, blank=True)
    longitude = models.BigIntegerField(null=True, blank=True)
    address = models.TextField( null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, default='pending', max_length=20)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    
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
    

    
    
    
class sportPrice(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)

class turfFacility(models.Model):
    facilities = models.ForeignKey(Facilities, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)


class Booking(models.Model):
    sport = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    hour = models.CharField(max_length=20, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    payment_option = models.CharField(max_length = 100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.BigIntegerField(null= True, blank=True)
    email = models.EmailField(null=True, blank=True)
    exists = models.BooleanField(default=False)
    status = models.CharField(null=True, blank=True, default='pending', max_length=20)
    # exists = models.CharField(max_length=20, null=True, blank=True, default='not')
    
 
