from django.shortcuts import render, redirect
from .models import Vehicle, Sticker
from django.shortcuts import render, redirect
from .models import Vehicle, Sticker


def sticker_management(request):
    stickers = Sticker.objects.all()  # Retrieve all stickers for management
    return render(request, 'sticker_management.html', {'stickers': stickers})


def home(request):
    vehicles = Vehicle.objects.all()
    stickers = Sticker.objects.all()
    return render(request, 'home.html', {
        'vehicles': vehicles,
        'stickers': stickers,
    })

def register_vehicle(request):
    if request.method == 'POST':
        vehicle = Vehicle(
            vehicleManufacturer=request.POST['manufacturer'],
            vehicleColor=request.POST['color'],
            vehicleType=request.POST['type']
        )
        vehicle.save()
        # Automatically assign a sticker (you can modify this logic as needed)
        Sticker.objects.create(
            purchaseDate=request.POST['purchase_date'],
            expiryDate=request.POST['expiry_date'],
            vehicle=vehicle
        )
        return redirect('home')
    return render(request, 'register_vehicle.html')

def edit_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if request.method == 'POST':
        vehicle.vehicleManufacturer = request.POST['manufacturer']
        vehicle.vehicleColor = request.POST['color']
        vehicle.vehicleType = request.POST['type']
        vehicle.save()
        return redirect('home')
    return render(request, 'edit_vehicle.html', {'vehicle': vehicle})

def delete_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return redirect('home')

def renew_sticker(request, sticker_id):
    sticker = Sticker.objects.get(id=sticker_id)
    if request.method == 'POST':
        sticker.expiryDate = request.POST['expiry_date']
        sticker.save()
        return redirect('home')
    return render(request, 'renew_sticker.html', {'sticker': sticker})
