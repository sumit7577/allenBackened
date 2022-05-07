from django.http import FileResponse, JsonResponse,HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def home(request):
    if request.method == "POST":
        try:
            username= request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username =username,password = password)
            if user is not None:
                Token.objects.get_or_create(user=user)
                token = Token.objects.get(user_id=user.id)
                return JsonResponse({"error":False,"message":token.key})
            else:
                return JsonResponse({"error":True,"message":"Please enter Valid username and passsword"},status=404)
        except Exception as e:
            return JsonResponse({"error":True,"message":"Please enter username and passsword"},status=500)
    else:
        return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)


@csrf_exempt
def Login(request):
    if request.method == "POST":
        token = request.headers.get("token")
        query  = User.objects.all().filter(auth_token=token)
        if query is not None:
            user = {"name":query[0].username,"email":query[0].email,"type":"something"}
            return JsonResponse({"error":False,"message":user},status=200)
        else:
            return JsonResponse({"error":True,"message":"Please enter Valid Token Key"},status=404)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)



def Verify(token):
    query = User.objects.all().filter(auth_token=token)
    if query is not None:
        return True
    else:
        return False



