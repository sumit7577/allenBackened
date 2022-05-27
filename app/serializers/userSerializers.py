from rest_framework import serializers
from ..models import Expense, Tenant,Rent,Landlord,Property

class TenantSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields= "__all__"


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"
        depth=1


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields= "__all__"
        depth=1


class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        depth=1
