from lib2to3.pytree import LeafPattern
from django.contrib import admin
from .models import Tenant,Property,Rent,Landlord,Expense



# Register your models here.

class PropertyAdmin(admin.ModelAdmin):
    pass

class RentAdmin(admin.ModelAdmin):
    list_display = ('Room_Renter_Name',"Apartment_Name","Payment_Amount","Payment_Date")

class LandlordAdmin(admin.ModelAdmin):
    pass

class ExpenseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tenant)
admin.site.register(Property,PropertyAdmin)
admin.site.register(Rent,RentAdmin)
admin.site.register(Landlord,LandlordAdmin)
admin.site.register(Expense,ExpenseAdmin)