from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User model
class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)  # Email is now part of User model
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


class Vehicle(models.Model):
    vehicleManufacturer = models.CharField(max_length=100)
    vehicleColor = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicleManufacturer} - {self.vehicleColor} - {self.vehicleType}"

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default-profile.jpg')

    def __str__(self):
        return f"{self.user.username} - Profile"


# Signal handlers outside of the model classes
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
