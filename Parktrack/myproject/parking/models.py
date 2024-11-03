from django.db import models

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=15)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Sticker(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='stickers', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, null=True)  # Temporarily make nullable
    expiration_date = models.DateField()  # Ensure this matches the new field name


    def __str__(self):
        return f"{self.color} Sticker for {self.vehicle}"
    