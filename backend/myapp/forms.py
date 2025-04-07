from django import forms
from .models import ParkingArea, ParkingLot, Reservation

class ParkingAreaForm(forms.ModelForm):
    class Meta:
        model = ParkingArea
        fields = ['parking_location']

class ParkingLotForm(forms.ModelForm):
    class Meta:
        model = ParkingLot
        fields = ['parking_lot_number', 'parking_lot_status']  # adjust based on your model

    def __init__(self, *args, **kwargs):
        # The parking_area should be passed as an argument
        self.parking_area = kwargs.pop('parking_area', None)
        super().__init__(*args, **kwargs)

    def clean_parking_lot_number(self):
        parking_lot_number = self.cleaned_data.get('parking_lot_number')

        # Check if a parking lot with this number already exists in the given parking area
        if self.parking_area and ParkingLot.objects.filter(parking_area=self.parking_area, parking_lot_number=parking_lot_number).exists():
            raise forms.ValidationError('A parking lot with this number already exists in this area.')

        return parking_lot_number
    

 
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['parking_area', 'parking_lot', 'entry_date', 'entry_time', 'exit_date', 'exit_time']

    # Dynamic queryset for parking lots based on selected parking area
    def __init__(self, *args, **kwargs):
        parking_area = kwargs.pop('parking_area', None)
        super().__init__(*args, **kwargs)
        if parking_area:
            self.fields['parking_lot'].queryset = ParkingLot.objects.filter(parking_area=parking_area, is_available=True)   