def get_base_context(request):
    user = request.user

    if user.is_authenticated:
        user_name = f"{user.first_name} {user.last_name}"
        user_fname = user.first_name
        user_role = user.groups.first().name if user.groups.exists() else 'Guest'
        vehicle = getattr(user, 'vehicle', None)
        vehicle_info = {
            "manufacturer": vehicle.vehicleManufacturer if vehicle else "None",
            "type": vehicle.vehicleType if vehicle else "N/A",
            "color": vehicle.vehicleColor if vehicle else "N/A",
            "plate_number": vehicle.plate_number if vehicle else "N/A",
            "image": vehicle.vehicleImage.url if vehicle and vehicle.vehicleImage else None,
        }
    else:
        user_name = "Guest"
        user_fname = "Guest"
        user_role = "Guest"
        vehicle_info = {
            "manufacturer": "None",
            "type": "N/A",
            "color": "N/A",
            "plate_number": "N/A",
            "image": None,
        }

    return {
        'user_name': user_name,
        'user_fname': user_fname,
        'user_role': user_role,
        'vehicle_info': vehicle_info,
    }

def get_base_context2(request):
    user = request.user

    if user.is_authenticated:
        user_name = f"{user.first_name} {user.last_name}"
        user_fname = user.first_name
        user_role = user.groups.first().name if user.groups.exists() else 'Guest'
        vehicle = getattr(user, 'vehicle', None)
        vehicle_id = getattr(vehicle, 'id', None) if vehicle else None
        vehicle_info = {
            "manufacturer": vehicle.vehicleManufacturer if vehicle else "None",
            "type": vehicle.vehicleType if vehicle else "N/A",
            "color": vehicle.vehicleColor if vehicle else "N/A",
            "plate_number": vehicle.plate_number if vehicle else "N/A",
            "image": vehicle.vehicleImage.url if vehicle and vehicle.vehicleImage else None,
        }
    else:
        user_name = "Guest"
        user_fname = "Guest"
        user_role = "Guest"
        vehicle_id = None
        vehicle_info = {
            "manufacturer": "None",
            "type": "N/A",
            "color": "N/A",
            "plate_number": "N/A",
            "image": None,
        }

    return {
        'user_name': user_name,
        'user_fname': user_fname,
        'user_role': user_role,
        'vehicle_info': vehicle_info,
        'vehicle_id': vehicle_id,  # Include the vehicle_id
    }

