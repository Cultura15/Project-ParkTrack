# parking/models.py

from datetime import date
from django.db import models

class Vehicle(models.Model):
    vehicleManufacturer = models.CharField(max_length=100)
    vehicleColor = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicleManufacturer} - {self.vehicleColor} - {self.vehicleType}"

class Sticker(models.Model):
    purchaseDate = models.DateField(default=date.today)
    expiryDate = models.DateField(default=date.today)  # Set a default value
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sticker - {self.purchaseDate} to {self.expiryDate}"
