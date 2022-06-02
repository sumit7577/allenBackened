from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import Verify,userCheck
from .models import Expense, Rent,Property,Tenant,Landlord
from .serializers import userSerializers
from django.db.models import Sum

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
                        return JsonResponse({"error":False,"message":{"rent":rentData.data,"expense":expenseData.data,"dashboard":queryData['dashboard']}})
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
            return JsonResponse({"error":True,"messag":"Please! Provide Auth Token"},status=200)
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
    totalPaid = rentData.aggregate(Sum("Payment_Amount"))
    totalExpensePaid  = expenseData.aggregate(Sum("Payment_Amount"))
    monthlyRent = 100
    AmountDeposited = 100
    dashboardData = {"Amount_Deposited":AmountDeposited,"Monthly_Rent":monthlyRent,"My_Expense":totalExpensePaid,"Total_Rent_Paid":totalPaid}
    response['rent'] = rentData
    response['expense'] = expenseData
    response['dashboard'] = dashboardData
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


@csrf_exempt
def editExpense(request):
    if request.method == "POST":
        try:
            token = request.headers['authorization']
            userCategory = userCheck(token)
            if userCategory[0] == "Landlord":
                id = request.POST.get("id")
                choices = request.POST.get("choice")
                message = request.POST.get("message")
                expenseData = Expense.objects.get(id=id)
                expenseData.Status = choices
                expenseData.Declined_Message = message
                expenseData.save()
                return JsonResponse({"error":False,"message":f"You {choices}ed This Expense"},status=200)
            else:
                return JsonResponse({"error":True,"message":"You are Not a Landlord To Edit This!"},status=200)
        except Exception as e:
            print(e)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=409)