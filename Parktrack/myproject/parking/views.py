# myproject/parking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehicle, Sticker
from .forms import VehicleForm, StickerForm
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

# Vehicle Views
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicle_form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})

# Sticker Views
def sticker_list(request):
    stickers = Sticker.objects.all()
    return render(request, 'sticker_list.html', {'stickers': stickers})

def sticker_create(request):
    if request.method == 'POST':
        form = StickerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sticker_list')
    else:
        form = StickerForm()
    return render(request, 'sticker_form.html', {'form': form})

def sticker_update(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    if request.method == 'POST':
        form = StickerForm(request.POST, instance=sticker)
        if form.is_valid():
            form.save()
            return redirect('sticker_list')
    else:
        form = StickerForm(instance=sticker)
    return render(request, 'sticker_form.html', {'form': form})

def sticker_delete(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    if request.method == 'POST':
        sticker.delete()
        return redirect('sticker_list')
    return render(request, 'sticker_confirm_delete.html', {'sticker': sticker})
