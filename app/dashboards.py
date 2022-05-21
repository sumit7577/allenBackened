from pydoc import apropos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import Verify,userCheck
from .models import Expense, Rent,Property,Tenant
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
                        
                    elif userType[0] == "Landlord":
                        queryData = Landlord(token,userType[1])
                        return JsonResponse({"error":True,"message":"Not Valid"})
                    else:
                        return JsonResponse({"error":True,"message":"Not Valid"})
                    return JsonResponse({"error":False,"message":{"rent":rentData.data,"expense":expenseData.data}})
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
                Test  = Expense.objects.create(Expense_User=userInfo,Invoice=invoice,Category=category,Payment_Amount=amount,Apartment_Name=apartmentInfo,Title=expenseTitle)
                print(Test)
                return JsonResponse({"error":False,"message":"New Request SuccessFull!"},status=200)
            else:
                pass
        except Exception as e:
            print(e)
            return JsonResponse({"error":True,"message":"Please! Provide Auth Token!"},status=500)

    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)