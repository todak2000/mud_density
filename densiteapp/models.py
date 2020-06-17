from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class appUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    company = models.TextField(max_length=200,verbose_name="Company")
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user} - {self.firstname} - {self.lastname} - {self.email} - {self.company} - {self.date_added_normal} - {self.user_password}"


class waterMudCalculation(models.Model):
    pressure = models.DecimalField(verbose_name="Downhole Pressure",blank=True, decimal_places=2, max_digits=10)
    temperature = models.DecimalField(verbose_name="Downhole Temperature",blank=True, decimal_places=2, max_digits=10)
    initial_density = models.DecimalField(verbose_name="Initial Mud Density",blank=True, decimal_places=2, max_digits=4)
    final_density = models.DecimalField(verbose_name="Final Mud Density",blank=True, decimal_places=2, max_digits=4)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.pressure} - {self.temperature} - {self.initial_density} - {self.final_density}"



class oilMudCalculation(models.Model):
    pressure = models.DecimalField(verbose_name="Downhole Pressure",blank=True, decimal_places=2, max_digits=10)
    temperature = models.DecimalField(verbose_name="Downhole Temperature",blank=True, decimal_places=2, max_digits=10)
    initial_density = models.DecimalField(verbose_name="Initial Mud Density",blank=True, decimal_places=2, max_digits=4)
    final_density = models.DecimalField(verbose_name="Final Mud Density",blank=True, decimal_places=2, max_digits=4)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.pressure} - {self.temperature} - {self.initial_density} - {self.final_density}"

class dashboardTable(models.Model):
    pressure = models.DecimalField(verbose_name="Downhole Pressure",blank=True, decimal_places=2, max_digits=10)
    temperature = models.DecimalField(verbose_name="Downhole Temperature",blank=True, decimal_places=2, max_digits=10)
    initial_density = models.DecimalField(verbose_name="Initial Mud Density",blank=True, decimal_places=2, max_digits=4)
    final_density = models.DecimalField(verbose_name="Final Mud Density",blank=True, decimal_places=2, max_digits=4)
    type_model = models.CharField(verbose_name="Type of Model",blank=True, max_length=30)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.pressure} - {self.temperature} - {self.initial_density} - {self.final_density} - {self.type_model}"