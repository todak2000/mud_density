from django.contrib import admin
from .models import appUser,waterMudCalculation,oilMudCalculation,dashboardTable

# Register your models here.
admin.site.register(appUser)
admin.site.register(waterMudCalculation)
admin.site.register(oilMudCalculation)
admin.site.register(dashboardTable)