from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from .models import appUser,waterMudCalculation,oilMudCalculation,dashboardTable
from django.contrib.auth import login,logout, authenticate
# Create your views here.

# Landing page
def index(request):
    return render(request,"login.html") 

# Signout
def signout(request):
    logout(request)
    return render(request,"login.html") 

# register page
def register(request):
    return render(request,"register.html") 

# water-based calculation page
def water(request):
    return_data = {
        "user":request.user,
        # "unreadMsg": unreadMessages,
        # "allocatedWasteCoins": totalCoins,
        # "minedCoins": minedCoins,
        "appuser": appUser.objects.filter(user=request.user),
        # "miner": miners,
        }
    return render(request,"water.html", return_data)

# oil-based calculation page
def oil(request):
    return_data = {
        "user":request.user,
        # "unreadMsg": unreadMessages,
        # "allocatedWasteCoins": totalCoins,
        # "minedCoins": minedCoins,
        "appuser": appUser.objects.filter(user=request.user),
        # "miner": miners,
        }
    return render(request,"oil.html", return_data)

# user registration api
@api_view(["POST"])
def registrationapi(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        confirmPassword = request.data.get('confirmPassword',None)
        company = request.data.get('company',None)
        
        reg_field = [firstName,lastName,email,password,confirmPassword,company]
        if not None in reg_field and not "" in reg_field:
            if User.objects.filter(email =email).exists():
                return_data = {
                    "error": "1",
                    "message": "User Exists"
                }
            if password != confirmPassword:
                return_data = {
                    "error": "1",
                    "message": "Password is not the same"
                }
            else:
                user=User.objects.create_user(email, email,password)
                user.first_name=firstName
                user.last_name=lastName
                user.save()
                registerUser = appUser(user=user, firstname=firstName, lastname=lastName, email=email,company=company,user_password=password) 
                registerUser.save()
                
                return_data = {
                    "error": "0",
                    "message":"The registration was successful.",
                    }
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"register.html", return_data) 

# User login api
@api_view(["POST"])
def loginapi(request):
    email=request.POST["email"]
    password=request.POST["password"]
    user = authenticate(request,username=email, password=password)

    if  user is None:
         return render(request,"login.html",{"message":"Sorry! User do not exist. Please Contact the technical team. Thanks"})
   
    if user is not None:
        login(request,user)
        currentUser = appUser.objects.filter(user=request.user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request,"login.html",{"message":"Invalid credentials"})

# dashboard view page
def dashboard(request):
    table_list = dashboardTable.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(table_list, 3)
    try:
        table = paginator.page(page)
    except PageNotAnInteger:
        table = paginator.page(1)
    except EmptyPage:
        table = paginator.page(paginator.num_pages)
    return_data = {
        # "user":request.user,
        # "unreadMsg": unreadMessages,
        # "allocatedWasteCoins": totalCoins,
        # "table_list": table_list,
        "appuser": appUser.objects.filter(user=request.user),
        "table": table
        }
    return render(request,"dashboard.html", return_data) 

# water-based mud calcuation api
@api_view(["POST"])
def waterapi(request):
    pressure=float(request.POST["pressure"])
    temperature=float(request.POST["temperature"])
    initial_density=float(request.POST["initial_density"])
    '''
    The Model formula for Water-based Density calculation takes
    @parameters: Pressure (P), Temperature (T) and Initial Density(D) into this formula 
    below:
    3.51 + 0.43(D) + 0.00000991(P) + 0.00000227(P)(D) + 0.0218(D^2) - 0.000133(T)(D) - 0.00000566(T^2)
    '''
    a = 3.51
    b = 0.43*initial_density
    c = 0.00000991*pressure
    d = 0.00000227*pressure*initial_density
    e = 0.0218*initial_density**2
    f = 0.000133*temperature*initial_density
    g = 0.00000566*temperature**2
    water_final_density = a + b + c + d + e - f - g

    saveWaterInput = waterMudCalculation(pressure=pressure, temperature=temperature, initial_density=initial_density, final_density=water_final_density) 
    saveWaterInput.save()
    saveDashboardTable = dashboardTable(pressure=pressure, temperature=temperature, initial_density=initial_density, final_density=water_final_density, type_model="Water-Based") 
    saveDashboardTable.save()
    return_data = {
        # "user":request.user,
        "appuser": appUser.objects.filter(user=request.user),
        "water_final_density": water_final_density
    }
    return render(request,"water.html",return_data)

# oil-based mud calcuation api
@api_view(["POST"])
def oilapi(request):
    pressure=float(request.POST["pressure"])
    temperature=float(request.POST["temperature"])
    initial_density=float(request.POST["initial_density"])
    '''
    The Model formula for Oil-based Density calculation takes
    @parameters: Pressure (P), Temperature (T) and Initial Density(D) into this formula 
    below:
    9.49 + 0.689(D) + 0.00016(P) + 0.0000000000141(T)(P^2) + ((-63.7 - 0.000689(P))/D) - 0.00337(T) - 0.0000975(T)(D) - 0.00000000712(P^2)
    '''
    a = 9.49
    b = 0.689*initial_density
    c = 0.00016*pressure
    d = 0.0000000000141*pressure**2*temperature
    e = ((-63.7 - 0.000689*pressure)/initial_density) 
    f = 0.00337*temperature
    g = 0.0000975*temperature*initial_density
    h = 0.00000000712*pressure**2
    oil_final_density = a + b + c + d + e - f - g -h 

    saveOilInput = oilMudCalculation(pressure=pressure, temperature=temperature, initial_density=initial_density, final_density=oil_final_density) 
    saveOilInput.save()
    saveDashboardTable = dashboardTable(pressure=pressure, temperature=temperature, initial_density=initial_density, final_density=oil_final_density, type_model="Oil-Based") 
    saveDashboardTable.save()
    return_data = {
        # "user":request.user,
        "appuser": appUser.objects.filter(user=request.user),
        "oil_final_density": oil_final_density
    }
    return render(request,"oil.html",return_data)