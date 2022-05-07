from django.http import FileResponse, JsonResponse,HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .views import Verify

@csrf_exempt
def dashboard(request):
    if request.method == "POST":
        try:
            token = request.headers['token']
            if Verify(token=token):
                return JsonResponse({"error":False,"messag":"Login Done"})
            else:
                return JsonResponse({"error":True,"messag":"Not Allowed"})
        except Exception as e:
            return JsonResponse({"error":True,"messag":"Please! Provide Auth Token"},status=500)
    return JsonResponse({"error":True,"message":"Get Method Not Allowed!"},status=500)