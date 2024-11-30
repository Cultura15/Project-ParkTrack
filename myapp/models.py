from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


    ### USER ###

class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    contactNo = models.CharField(max_length=15)
    accountType = models.CharField(choices=[('staff', 'Staff'), ('user', 'User')], max_length=10)

    vehicle = models.ForeignKey(
        'myapp.Vehicle',  # Replace 'myapp' with your app name
        on_delete=models.SET_NULL,  # Set to NULL if the vehicle is deleted
        null=True,  # Allows the field to be optional
        blank=True,  # Allows the field to be left blank in forms
        related_name='users'
    )

    class Meta:
        db_table = 'myapp_user'  # Replace 'myapp' with your actual app name
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
    
    
    
    ### VEHICLE ###

class Vehicle(models.Model):
    vehicleId = models.AutoField(primary_key=True)
    vehicleManufacturer = models.CharField(max_length=100)
    vehicleColor = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50)
    vehicleImage = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    plate_number = models.CharField(max_length=20, unique=True)
    is_equipped = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='vehicles')  # Add this line

    def __str__(self):
        return f"{self.vehicleManufacturer} - {self.vehicleColor} - {self.vehicleType} - {self.plate_number}"


    class Meta:
        db_table = 'myapp_vehicle'  # Custom table name, optional
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'


class Sticker(models.Model):
    purchaseDate = models.DateField(default=date.today)
    expiryDate = models.DateField(default=date.today)  # Set a default value
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sticker - {self.purchaseDate} to {self.expiryDate}"

    class Meta:
        db_table = 'myapp_sticker'  # Custom table name, optional
        verbose_name = 'sticker'
        verbose_name_plural = 'stickers'


    ### PARKING AREA ###

class ParkingArea(models.Model):
    parking_area_id = models.AutoField(primary_key=True)
    parking_location = models.CharField(max_length=100)

    def __str__(self):
        return self.parking_location

class ParkingLot(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied')
    ]

    parking_lot_id = models.AutoField(primary_key=True)
    parking_area = models.ForeignKey('ParkingArea', related_name='parking_lots', on_delete=models.CASCADE)
    parking_lot_number = models.CharField(max_length=10)
    parking_lot_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)  # ForeignKey to User
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.SET_NULL)  # ForeignKey to Vehicle

    def save(self, *args, **kwargs):
        if not self.pk and self.parking_area.parking_lots.count() >= 10:
            raise ValidationError("Each parking area can only have 10 parking lots.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lot {self.parking_lot_number} - {self.parking_lot_status} (Area: {self.parking_area})"
    

class Reservation(models.Model):
    parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    entry_date = models.DateField()
    entry_time = models.TimeField()
    exit_date = models.DateField()
    exit_time = models.TimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation for Lot {self.parking_lot.parking_lot_number} in {self.parking_area.name}"    