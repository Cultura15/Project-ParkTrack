from django import forms
from .models import ParkingArea, ParkingLot

class ParkingAreaForm(forms.ModelForm):
    class Meta:
        model = ParkingArea
        fields = ['parking_location']

class ParkingLotForm(forms.ModelForm):
    PARKING_LOT_NUMBER_CHOICES = [(i, f"Lot {i}") for i in range(1, 11)]  # Choices from 1 to 10

    parking_lot_number = forms.ChoiceField(choices=PARKING_LOT_NUMBER_CHOICES)

    class Meta:
        model = ParkingLot  # Replace with your actual model name
        fields = ['parking_lot_number', 'parking_lot_status']  # Adjust fields as necessary