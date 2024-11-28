from rest_framework import serializers
from .models import ParkingArea, ParkingLot

class ParkingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingArea
        fields = ['parking_area_id', 'parking_location']

class ParkingLotSerializer(serializers.ModelSerializer):
    parking_area = ParkingAreaSerializer()  # Include ParkingArea details in the ParkingLot serialization

    class Meta:
        model = ParkingLot
        fields = ['parking_lot_id', 'parking_area', 'parking_lot_number', 'parking_lot_status']
