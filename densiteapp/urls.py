from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register", views.register, name="register"),
    path("registerapi", views.registrationapi, name="registerapi"),
    path("loginapi", views.loginapi, name="loginapi"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("water", views.water, name="water"),
    path("oil", views.oil, name="oil"),
    path("signout", views.signout, name="signout"),
    path("waterapi", views.waterapi, name="waterapi"),
    path("oilapi", views.oilapi, name="oilapi"),
    
]

