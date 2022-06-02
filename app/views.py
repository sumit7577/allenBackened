from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from app.models import Landlord, Tenant


# Create your views here.
@csrf_exempt
def home(request):
    if request.method == "POST":
        try:
            username= request.POST.get("username")
            password = request.POST.get("password")
            type = request.POST.get("type")
            user = authenticate(username =username,password = password)
            if user is not None:
                Token.objects.get_or_create(user=user)
                token = Token.objects.get(user_id=user.id)
                userType= userCheck(token)
                if userType[0] == type:
                    return JsonResponse({"error":False,"message":token.key})
                else:
                    return JsonResponse({"error":True,"message":f"This User is Not Assigned as {type}"})
            else:
                return JsonResponse({"error":True,"message":"Please enter Valid username and passsword"},status=200)
        except Exception as e:
            return JsonResponse({"error":True,"message":"Please enter username and passsword"},status=200)
    else:
        return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)


@csrf_exempt
def Login(request):
    if request.method == "POST":
        token = request.headers.get("authorization")
        query  = User.objects.all().filter(auth_token=token)
        if len(query) >0:
            getUser = userCheck(token)
            user = {"name":query[0].username,"email":query[0].email,"type":getUser[0]}
            return JsonResponse({"error":False,"message":user},status=200)
        else:
            return JsonResponse({"error":True,"message":"Please enter Valid Token Key"},status=200)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)



def Verify(token):
    query = User.objects.all().filter(auth_token=token)
    if query is not None:
        return True
    else:
        return False


def userCheck(token):
    user = (None,None)
    tenatUser= Tenant.objects.filter(user__auth_token= token)
    if len(tenatUser)> 0:
        user = ("Tenant",tenatUser[0])
    else:
        query = Landlord.objects.filter(user__auth_token= token)
        if len(query) >0:
            user = ("Landlord",query[0].id)
    return user




