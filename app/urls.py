from django.urls import path
from app import views
from app.dashboards import dashboard

urlpatterns = [
    # The home page
    path("",views.home,name="home"),
    path("verify",views.Login,name="verify"),
    path("dashboard",dashboard,name="Dashboard")
]