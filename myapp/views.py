from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import ParkingArea, ParkingLot
from .forms import ParkingAreaForm, ParkingLotForm

# Parking Area Views
def parking_area_list(request):
    parking_areas = ParkingArea.objects.all()
    return render(request, 'myapp/parking_area_list.html', {'parking_areas': parking_areas})

def parking_area_create(request):
    if request.method == 'POST':
        form = ParkingAreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parking_area_list')  # Update this if necessary
    else:
        form = ParkingAreaForm()
    return render(request, 'myapp/parking_area_form.html', {'form': form})

def parking_area_update(request, pk):
    area = get_object_or_404(ParkingArea, pk=pk)
    if request.method == 'POST':
        form = ParkingAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('parking_area_list')  # Update this if necessary
    else:
        form = ParkingAreaForm(instance=area)
    return render(request, 'myapp/parking_area_form.html', {'form': form, 'area': area})

def parking_area_delete(request, pk):
    area = get_object_or_404(ParkingArea, pk=pk)
    if request.method == 'POST':
        area.delete()
        return redirect('parking_area_list')
    return render(request, 'myapp/parking_area_confirm_delete.html', {'parking_area': area})

# Parking Lot Views
def parking_lot_list(request):
    # Group lots by their parking area to see the 10-space structure for each area
    parking_areas = ParkingArea.objects.prefetch_related('parking_lots')
    return render(request, 'myapp/parking_lot_list.html', {'parking_areas': parking_areas})

def parking_lot_create(request, area_id):
    parking_area = get_object_or_404(ParkingArea, pk=area_id)
    
    if request.method == 'POST':
        form = ParkingLotForm(request.POST)
        if form.is_valid():
            parking_lot = form.save(commit=False)
            parking_lot.parking_area = parking_area
            
            if ParkingLot.objects.filter(parking_area=parking_area, parking_lot_number=parking_lot.parking_lot_number).exists():
                return render(request, 'myapp/parking_lot_form.html', {
                    'form': form,
                    'parking_area': parking_area,
                    'existing_lot_numbers': ParkingLot.objects.filter(parking_area=parking_area).values_list('parking_lot_number', flat=True),
                    'error_message': "A parking lot with this number already exists in this area.",
                })

            if parking_area.parking_lots.count() >= 10:
                return render(request, 'myapp/parking_lot_form.html', {
                    'form': form,
                    'parking_area': parking_area,
                    'existing_lot_numbers': ParkingLot.objects.filter(parking_area=parking_area).values_list('parking_lot_number', flat=True),
                    'error_message': "This parking area already has 10 parking lots.",
                })

            parking_lot.save()
            return redirect('parking_lot_list')
    else:
        form = ParkingLotForm()

    existing_lot_numbers = ParkingLot.objects.filter(parking_area=parking_area).values_list('parking_lot_number', flat=True)

    return render(request, 'myapp/parking_lot_form.html', {
        'form': form,
        'parking_area': parking_area,
        'existing_lot_numbers': existing_lot_numbers,  # Pass existing lot numbers to the template
    })


def parking_lot_update(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    if request.method == 'POST':
        form = ParkingLotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            return redirect('parking_lot_list')  # Update this if necessary
    else:
        form = ParkingLotForm(instance=lot)
    return render(request, 'myapp/parking_lot_form.html', {'form': form, 'lot': lot})

def parking_lot_delete(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    if request.method == 'POST':
        lot.delete()
        return redirect('parking_lot_list')
    return render(request, 'myapp/parking_lot_confirm_delete.html', {'parking_lot': lot})

# Toggle Parking Lot Status View
@require_POST
def toggle_parking_lot_status(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    lot.parking_lot_status = 'occupied' if lot.parking_lot_status == 'vacant' else 'vacant'
    lot.save()
    return redirect(reverse('parking_area_list'))  # Adjust if the redirect should be to a specific area
