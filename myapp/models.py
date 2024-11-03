from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    contactNo = models.CharField(max_length=15)
    accountType = models.CharField(choices=[('staff', 'Staff'), ('user', 'User')], max_length=10)

    class Meta:
        db_table = 'myapp_user'  # Replace 'myapp' with your actual app name
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

class Sticker(models.Model):
    stickerId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchaseDate = models.DateField()
    expiryDate = models.DateField()

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('2 wheels', '2 Wheels'),
        ('4 wheels', '4 Wheels'),
    ]
    vehicleId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sticker = models.ForeignKey(Sticker, on_delete=models.SET_NULL, null=True)
    vehicleManufacturer = models.CharField(max_length=50)
    vehicleColor = models.CharField(max_length=20)
    vehicleType = models.CharField(max_length=10, choices=VEHICLE_TYPES)

class ParkingArea(models.Model):
    parkingArea_id = models.AutoField(primary_key=True)
    parkingLocation = models.CharField(max_length=255)

class ParkingLot(models.Model):
    PARKING_STATUS = [
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
    ]
    parkingLot_id = models.AutoField(primary_key=True)
    parkingArea = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    parkingLotNumber = models.IntegerField()
    parkingLotStatus = models.CharField(max_length=10, choices=PARKING_STATUS)
