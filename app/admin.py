from attr import field
from django.contrib import admin
from .models import Tenant,Property,Rent



# Register your models here.

class PropertyAdmin(admin.ModelAdmin):
    pass

class RentAdmin(admin.ModelAdmin):
    list_display = ('Room_Renter_Name',"Apartment_Name","Payment_Amount","Payment_Date")

admin.site.register(Tenant)
admin.site.register(Property,PropertyAdmin)
admin.site.register(Rent,RentAdmin)