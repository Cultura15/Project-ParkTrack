# parking/serializers.py
from rest_framework import serializers
from .models import Vehicle, Sticker

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = '__all__'
