from django.db import models

# Create your models here.


class Facilities(models.Model):
    facility = models.CharField(max_length=20, null=True, blank=True)
    
    
class Category(models.Model):
    sport = models.CharField(max_length=20, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)
    
    
    @property
    def ImageURL3(self):
        try:
            url = self.icon.url
        except:
            url = ''
        return url
    
