from django import forms
from .models import Vehicle, Sticker

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_manufacturer', 'vehicle_color', 'vehicle_type', 'plate_number']

class StickerForm(forms.ModelForm):
    class Meta:
        model = Sticker
        fields = ['purchase_date', 'expiry_date']
