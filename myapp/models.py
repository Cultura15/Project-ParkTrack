from django.db import models
from django.core.exceptions import ValidationError

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
    parking_area = models.ForeignKey(ParkingArea, related_name='parking_lots', on_delete=models.CASCADE)
    parking_lot_number = models.CharField(max_length=10)
    parking_lot_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def save(self, *args, **kwargs):
        # Check if the parking area already has 10 lots
        if self.parking_area.parking_lots.count() >= 10:
            raise ValidationError("Each parking area can only have 10 parking lots.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lot {self.parking_lot_number} - {self.parking_lot_status} (Area: {self.parking_area})"
