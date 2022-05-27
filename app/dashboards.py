from multiprocessing import managers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import Verify,userCheck
from .models import Expense, Rent,Property,Tenant,Landlord
from .serializers import userSerializers

@csrf_exempt
def dashboard(request):
    if request.method == "POST":
        try:
            token = request.headers['authorization']
            if Verify(token=token):
                userType = userCheck(token)
                if userType[0] is not None and userType[1] is not None:
                    if userType[0] == "Tenant":
                        queryData = TenantFunc(token,userType[1])
                        rentData = userSerializers.RentSerializer(queryData['rent'],many=True)
                        expenseData = userSerializers.ExpenseSerializer(queryData['expense'],many=True)
                        return JsonResponse({"error":False,"message":{"rent":rentData.data,"expense":expenseData.data}})
                    elif userType[0] == "Landlord":
                        queryData = LandlordFunc(token,userType[1])
                        expenseData = userSerializers.ExpenseSerializer(queryData['expense'],many=True)
                        apartmentData = userSerializers.PropertySerializer(queryData['apartment'],many=True)
                        rentData = userSerializers.RentSerializer(queryData['rent'],many=True)
                        return JsonResponse({"error":False,"message":{"expense":expenseData.data,"apartment":apartmentData.data,"rent":rentData.data}})
                    else:
                        return JsonResponse({"error":True,"message":"Not Valid"})
                else:
                    return JsonResponse({"error":True,"messag":"Please Assign This User as a Landlord or Tenant"})
            else:
                return JsonResponse({"error":True,"messag":"Not Allowed"})
        except Exception as e:
            print(e)
            return JsonResponse({"error":True,"messag":"Please! Provide Auth Token"},status=500)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)



def LandlordFunc(token,id):
    response = {}
    landlordName = Landlord.objects.filter(id=id)
    expenseData = Expense.objects.select_related("Apartment_Name").filter(Apartment_Name__Apartment_Owner_id=landlordName[0].id)
    apartmentData = Property.objects.select_related("Apartment_Owner").filter(Apartment_Owner=landlordName[0])
    rentData = Rent.objects.select_related("Apartment_Name").filter(Apartment_Name__Apartment_Owner_id=landlordName[0].id)
    response["expense"] = expenseData
    response["apartment"]  = apartmentData
    response['rent'] = rentData
    return response



def TenantFunc(token,id):
    response = {}
    propertyName = Property.objects.filter(Room_Renter=id)
    rentData = Rent.objects.filter(Apartment_Name_id=propertyName[0].id)
    expenseData = Expense.objects.filter(Apartment_Name_id=rentData[0].id)
    response['rent'] = rentData
    response['expense'] = expenseData
    return response

@csrf_exempt
def addExpense(request):
    if request.method == "POST":
        try:
            token = request.headers['authorization']
            if Verify(token=token):
                username = request.POST.get("username")
                apartmentName = request.POST.get("apartment")
                expenseTitle = request.POST.get("title")
                amount = request.POST.get("amount")
                category = request.POST.get("category")
                invoice = request.FILES.get("invoice")
                userInfo = Tenant.objects.get(id=username)
                apartmentInfo = Property.objects.get(id=apartmentName)
                Expense.objects.create(Expense_User=userInfo,Invoice=invoice,Category=category,Payment_Amount=amount,Apartment_Name=apartmentInfo,Title=expenseTitle)
                return JsonResponse({"error":False,"message":"New Request SuccessFully Placed!"},status=200)
            else:
                return JsonResponse({"error":True,"message":"Please! Provide Auth Token!"},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"error":True,"message":"Please! Fill All Details Correctly"},status=200)

    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=409)