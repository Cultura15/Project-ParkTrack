# myproject/parking/forms.py
from django import forms
from .models import Vehicle, Sticker

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'make', 'model', 'year']

class StickerForm(forms.ModelForm):
    class Meta:
        model = Sticker
        fields = ['color', 'expiration_date', 'vehicle']
