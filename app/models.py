from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Tenant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=False,db_index=True)
    Profile_Image = models.ImageField(upload_to="profile",blank=True)

    def __str__(self):
        return self.user.username

    def save(self,*args,**kwargs):
        userCheck = User.objects.filter(landlord=self.user.id)
        if len(userCheck) > 0:
            raise ValueError(f"The {self.user.username} is Already Assigned as Landlord")
        else:
            super(Tenant,self).save(*args,**kwargs)


class Landlord(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=False,db_index=True)
    Profile_Image = models.ImageField(upload_to="profile",blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self,*args,**kwargs):
        userCheck = Tenant.objects.filter(user_id=self.user.id)
        if len(userCheck) > 0:
            raise ValueError(f"The {self.user.username} is Already Assigned as Tenants")
        else:
            super(Landlord,self).save(*args,**kwargs)


        
class Property(models.Model):
    name = models.CharField(max_length=120,blank=False,unique=True)
    apartment_Image = models.ImageField(upload_to="apartment",blank=True)
    Apartment_Owner = models.ForeignKey(Landlord,on_delete=models.CASCADE,related_name="owner_name")
    Room_Renter = models.ManyToManyField(Tenant,related_name="renter")
    Location= models.CharField(max_length=300,blank=False,unique=False)
    Room_Rent_Amount = models.IntegerField(blank=False,null=False)

    def __str__(self) -> str:
        return self.name



class Rent(models.Model):
    rentChoice = [
        ("Paid","Paid"),
        ("Not Paid","Not Paid")
    ]
    Room_Renter_Name = models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name='renter_name')
    Apartment_Name = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='apartment_name')
    Payment_Date = models.DateField(default=timezone.now)
    Status = models.CharField(choices=rentChoice,default="Not Paid",max_length=20)
    Payment_Amount = models.IntegerField(null=False,blank=False,unique=False)
    Currency_Code = models.CharField(blank=False,max_length=6,null=False,unique=False)
    
    def __str__(self) -> str:
        return self.Apartment_Name.name


    def save(self,*args,**kwargs):
        currentDate = timezone.now()
        propertyData = Property.objects.filter(Room_Renter__id=self.Room_Renter_Name_id,id=self.Apartment_Name_id)
        if len(propertyData) > 0:
            if self.Payment_Date.month == currentDate.month:
                try:
                    super(Rent,self).delete()
                    super(Rent,self).save(*args,**kwargs)
                except:
                    raise ValueError(f"The {self.Room_Renter_Name} Is Already Created Rent Object In This Month")
            else:
                super(Rent,self).save(*args,**kwargs)
        else:
            raise ValueError(f"The {self.Room_Renter_Name} user is not a Room Renter in {self.Apartment_Name} Property")


class Expense(models.Model):
    statusChoice = [
        ("Approved","Approved"),
        ("Requested","Requested"),
        ("Declined","Declined")
    ]
    Title = models.CharField(max_length=120,default="Maintainance invoice",blank=False,unique=False)
    Expense_User = models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name="expense_user")
    Payment_Date = models.DateField(default=timezone.now)
    Invoice = models.FileField(upload_to='invoice')
    Category = models.CharField(max_length=50,default="",blank=False,unique=False)
    Payment_Amount = models.IntegerField(blank=False,default=False)
    Apartment_Name = models.ForeignKey(Property,on_delete=models.CASCADE,related_name="expense_apartment")
    Status = models.CharField(choices=statusChoice,default="Requested",max_length=20)
    Declined_Message = models.CharField(default="",blank=True,null=True,max_length=200)
    Currency_Code = models.CharField(blank=False,max_length=6,null=False,unique=False)

    def __str__(self):
        return self.Title