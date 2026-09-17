from django.db import models

# Create your models here.
class AdminDetails(models.Model):
    username=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=100)
class CustomerDetails(models.Model):
    username=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=100)
class DriverDetails(models.Model):
    username=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='available')
class Location(models.Model):
    location=models.CharField(max_length=100, unique=True)
    km=models.IntegerField(default=400)
class OrderDetails(models.Model):
    name=models.CharField(max_length=100)
    from_location=models.CharField(max_length=100, default='chennai')
    to_location=models.CharField(max_length=100)
    customer_id=models.IntegerField()
    Driver_id=models.IntegerField(default=0)
    Driver_name=models.CharField(max_length=100, default='not assinged')
    status=models.CharField(max_length=100, default='processing')
    weight=models.IntegerField()
    product=models.CharField(max_length=100)

