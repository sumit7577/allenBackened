from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import Verify,userCheck
from .models import Rent,Property
from .serializers import userSerializers

@csrf_exempt
def dashboard(request):
    print(request)
    if request.method == "POST":
        try:
            token = request.headers['token']
            print(request.headers)
            if Verify(token=token):
                userType = userCheck(token)
                if userType[0] is not None and userType[1] is not None:
                    if userType[0] == "Tenant":
                        queryData = Tenant(token,userType[1])
                        pickledData = userSerializers.RentSerializer(queryData,many=True)
                    elif userType[0] == "Landlord":
                        queryData = Landlord(token,userType[1])
                    else:
                        return JsonResponse({"error":True,"message":"Not Valid"})
                    return JsonResponse({"error":False,"message":pickledData.data})
                else:
                    return JsonResponse({"error":True,"messag":"Please Assign This User as a Landlord or Tenant"})
            else:
                return JsonResponse({"error":True,"messag":"Not Allowed"})
        except Exception as e:
            print(e)
            return JsonResponse({"error":True,"messag":"Please! Provide Auth Token"},status=500)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)



def Landlord(token,id):
    apartmentData = Property.objects.filter(id=id)
    return apartmentData



def Tenant(token,id):
    rentData = Rent.objects.filter(id=id)
    return rentData