from attr import field
from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.utils import timezone



LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
# Create your models here.

class Tenant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=12,unique=False,db_index=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    def __str__(self):
        return self.user.username


class Property(models.Model):
    name = models.CharField(max_length=80,blank=False,unique=True)
    apartment_Image = models.ImageField(upload_to="apartment",blank=True)
    Apartment_Owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner_name")
    Room_Renter = models.ManyToManyField(User,related_name="renter_name")
    Location= models.CharField(max_length=300,blank=False,unique=False)

    def __str__(self) -> str:
        return self.name

class Rent(models.Model):
    Room_Renter_Name = models.ForeignKey(User,on_delete=models.CASCADE)
    Apartment_Name = models.ForeignKey(Property,on_delete=models.CASCADE)
    Payment_Date = models.DateTimeField(default=timezone.now)
    Payment_Amount = models.IntegerField(null=False,blank=False,unique=False)
    Currency_Code = models.CharField(blank=False,max_length=6,null=False,unique=False)
    
    def __str__(self) -> str:
        return self.Apartment_Name.name