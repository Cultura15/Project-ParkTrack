from django.contrib import admin
from .models import User, ParkingArea, Sticker, Vehicle, ParkingLot

admin.site.register(User)
admin.site.register(ParkingArea)
admin.site.register(Sticker)
admin.site.register(Vehicle)
admin.site.register(ParkingLot)
