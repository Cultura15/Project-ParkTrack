# serializers.py
from rest_framework import serializers
from .models import ParkingArea, ParkingLot

class ParkingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingArea
        fields = '__all__'


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = '__all__'
