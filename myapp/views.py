from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, Http404, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages
from django.middleware.csrf import get_token
import json
import logging
import requests
from .utils import get_base_context, get_base_context2

from .models import User, Vehicle, Sticker, ParkingArea, ParkingLot, Reservation
from .forms import ParkingAreaForm, ParkingLotForm, ReservationForm
from rest_framework.decorators import api_view
from .serializers import ParkingLotSerializer


# Home localhost
def home(request):
    return render(request, 'home.html')

# api/register //POST
@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        try:
            user = User(
                fname=data.get('fname'),
                lname=data.get('lname'),
                email=data.get('email'),
                gender=data.get('gender'),
                address=data.get('address'),
                contactNo=data.get('contactNo'),
                accountType=data.get('accountType'),
                username=data.get('email'),
                password=make_password(data.get('password'))
            )
            user.save()
            return JsonResponse({'message': 'Registration successful!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_user_details(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        if user_id:
            try:
                user = User.objects.get(userId=user_id)
                user_data = {
                    'fname': user.fname,
                    'lname': user.lname,
                    'accountType': user.accountType,
                    'email': user.email
                }
                return JsonResponse({'user': user_data}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        return JsonResponse({'error': 'No userId provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# api/login 
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Get the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            # Authenticate manually if the email exists
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                user_data = {
                    'userId': user.userId,
                    'fname': user.fname,
                    'lname': user.lname,
                    'accountType': user.accountType,
                }
                return JsonResponse({'message': 'Login successful!', 'user': user_data}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'login.html')

    

# api/menu
def menu_view(request):
    user = request.user  # Get the logged-in user

    if user.is_authenticated:
        # Fetch user details
        user_name = f"{user.first_name} {user.last_name}"  # Combine first and last name
        user_fname = user.first_name
        user_role = user.groups.first().name if user.groups.exists() else 'Guest'  # Role based on groups, fallback to 'Guest'

        # Fetch associated vehicle
        vehicle = getattr(user, 'vehicle', None)  # Get user's vehicle if exists
        vehicle_info = {
            "manufacturer": vehicle.vehicleManufacturer if vehicle else "None",
            "type": vehicle.vehicleType if vehicle else "N/A",
            "color": vehicle.vehicleColor if vehicle else "N/A",
            "plate_number": vehicle.plate_number if vehicle else "N/A",  # Placeholder plate info
            "image": vehicle.vehicleImage.url if vehicle and vehicle.vehicleImage else None,  # Vehicle image path
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
            "image": None,  # No image for guests
        }

    # Render the menu template with user and vehicle information
    return render(request, 'menu.html', {
        'user_name': user_name,
        'user_role': user_role,
        'user_fname': user_fname,
        'vehicle_info': vehicle_info,
    })







# api/users
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# api/users/<int:user_id> //GET & DELETE

@csrf_exempt
def user_detail(request, user_id):
    user = get_object_or_404(User, userId=user_id)

    if request.method == 'GET':
        # Return user details
        user_data = {
            'userId': user.userId,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email,
            'gender': user.gender,
            'address': user.address,
            'contactNo': user.contactNo,
            'accountType': user.accountType,
            'password' : user.password,
        }
        return JsonResponse(user_data, status=200)

    elif request.method == 'DELETE':
        # Delete user
        user.delete()
        return JsonResponse({'message': 'User deleted successfully!'}, status=204)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# api/users/<int:user_id> //GET & UPDATE
@require_http_methods(["GET", "POST"])
def update_user(request):
    user_id = request.GET.get('userId')  # Get userId from query parameters

    if request.method == 'GET':
        try:
            user = User.objects.get(userId=user_id)
            return render(request, 'update_user.html', {'user': user})  # Render the HTML template with user data
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    elif request.method == 'POST':
        try:
            user = User.objects.get(userId=user_id)
            user.fname = request.POST.get('fname', user.fname)
            user.lname = request.POST.get('lname', user.lname)
            user.email = request.POST.get('email', user.email)
            user.gender = request.POST.get('gender', user.gender)
            user.address = request.POST.get('address', user.address)
            user.contactNo = request.POST.get('contactNo', user.contactNo)
            user.password = request.POST.get('password' , user.password)
            user.accountType = request.POST.get('accountType', user.accountType)
            user.save()

            return JsonResponse({'success': 'User updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        

####### NAVIGATION #####

def base_view1(request):
    context = get_base_context(request)
    return render(request, 'base.html', context)

def parkingMap(request):
    context = get_base_context(request)
    return render(request, 'parkingMap.html', context)

def aboutUs(request):
    context = get_base_context(request)
    return render(request, 'aboutus.html', context)

def parkReserve(request):
    context = get_base_context(request)
    return render(request, 'parkreserve.html', context)

def accountSettings(request):
    context = get_base_context(request)
    return render(request, 'account.html', context)

def news(request):
    context = get_base_context(request)
    return render(request, 'news.html', context)

def map_view(request):
    context1 = get_base_context(request)  # Base context with user-related data
    context = {
        'latitude': 10.295559,
        'longitude': 123.880658,
        'zoom': 10,
        'bounds': {
            'north': 10.295951988147875,
            'south': 10.293841944776801,
            'west': 123.87978786269375,
            'east': 123.8817703943783,
        }
    }
    # Merge context dictionaries
    context.update(context1)
    return render(request, 'tryingMap.html', context)


        




##############################################################################################################################################

##### VEHICLE #####

def sticker_management(request):
    try:    
        stickers = Sticker.objects.all()
    except Exception as e:
        logging.error(f"Error retrieving stickers: {e}")
        return HttpResponseServerError("Something went wrong while fetching stickers.")
    return render(request, 'sticker_management.html', {'stickers': stickers})


def sticker(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Filter vehicles and stickers by the logged-in user
    vehicles = Vehicle.objects.filter(user=request.user)
    stickers = Sticker.objects.filter(vehicle__in=vehicles)
    
    # Get additional context
    context1 = get_base_context(request)

    # Merge context with vehicles and stickers
    context = {
        'vehicles': vehicles,
        'stickers': stickers,
    }
    context.update(context1)

    return render(request, 'sticker.html', context)



def sticker_view(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Filter vehicles and stickers by user
    vehicles = Vehicle.objects.filter(user=request.user)
    equipped_vehicle = vehicles.filter(is_equipped=True).first()
    stickers = Sticker.objects.filter(vehicle__in=vehicles)
    
    return render(request, 'sticker.html', {
        'vehicles': vehicles,
        'stickers': stickers,
        'equipped_vehicle': equipped_vehicle,
    })




def register_vehicle(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')

        try:
            user = User.objects.get(userId=user_id)

            # Check if the user already has 3 vehicles
            if user.vehicles.count() >= 3:  # Use the related_name from the ForeignKey
                return JsonResponse({'error': 'You cannot register more than 3 vehicles.'}, status=400)

            # Handle optional vehicle image
            vehicle_image = request.FILES.get('vehicleImage')

            # Create the vehicle
            vehicle = Vehicle(
                vehicleManufacturer=request.POST['manufacturer'],
                vehicleColor=request.POST['color'],
                vehicleType=request.POST['type'],
                vehicleImage=vehicle_image,
                plate_number=request.POST['plate_number'],  # Assuming plate_number is provided
                user=user,  # Associate the user with the vehicle
            )
            vehicle.save()

            # Create a sticker for the vehicle
            Sticker.objects.create(
                purchaseDate=request.POST['purchase_date'],
                expiryDate=request.POST['expiry_date'],
                vehicle=vehicle,
            )

            # Check if the request is AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON response for AJAX
                return JsonResponse({
                    'id': vehicle.vehicleId,
                    'vehicleManufacturer': vehicle.vehicleManufacturer,
                    'vehicleType': vehicle.vehicleType,
                    'vehicleColor': vehicle.vehicleColor,
                    'vehicleImageUrl': vehicle.vehicleImage.url if vehicle.vehicleImage else None,
                })

            # For non-AJAX requests, redirect as usual
            return redirect('sticker_management')

        except User.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON error for AJAX
                return JsonResponse({'error': 'User not found.'}, status=400)
            else:
                return render(request, 'register_vehicle.html', {
                    'error': 'User not found. Please ensure you are logged in correctly.'
                })

    # For GET or other request methods
    return render(request, 'register_vehicle.html')


@csrf_exempt
def equip_vehicle(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)

            vehicle_id = data.get('vehicleId')  # Use vehicleId as per the naming convention
            is_equipped = data.get('isEquipped')  # Use isEquipped for the equipped status

            # Validate input
            if vehicle_id is None or is_equipped is None:
                return JsonResponse({'error': 'Invalid input data.'}, status=400)

            # Fetch the vehicle
            vehicle = get_object_or_404(Vehicle, vehicleId=vehicle_id)  # Use vehicleId to fetch vehicle

            # Find the user associated with the vehicle
            user = vehicle.user

            # Check if the user already has another equipped vehicle
            currently_equipped_vehicle = user.vehicles.filter(is_equipped=True).first()

            if is_equipped:
                if currently_equipped_vehicle:
                    # Unequip the currently equipped vehicle before equipping the new one
                    currently_equipped_vehicle.is_equipped = False
                    currently_equipped_vehicle.save()

                # Equip the new vehicle
                vehicle.is_equipped = True
                vehicle.save()

                # Update the user's vehicle to the newly equipped vehicle
                user.vehicle = vehicle
                user.save()

            else:
                # Unequip the current vehicle
                vehicle.is_equipped = False
                vehicle.save()

                # Clear the user's vehicle field if the vehicle is unequipped
                user.vehicle = None
                user.save()

            # Return the updated vehicle status in the response
            return JsonResponse({
                'vehicleId': vehicle.vehicleId,
                'isEquipped': vehicle.is_equipped,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)




def vehicle_details(request, vehicleId):
    try:
        vehicle = Vehicle.objects.get(vehicleId=vehicleId)  # Use vehicleId for lookup
        return JsonResponse({
            'vehicleId': vehicle.vehicleId,  # Use vehicleId
            'manufacturer': vehicle.vehicleManufacturer,
            'color': vehicle.vehicleColor,
            'type': vehicle.vehicleType,
            'isEquipped': vehicle.is_equipped,
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    
def get_equipped_vehicle(request):
    user_id = request.GET.get('userId')
    
    if user_id:
        try:
            user = User.objects.get(userId=user_id)  # Use userId instead of id
            vehicle = user.vehicle  # Assuming you have a 'vehicle' related field
            if vehicle:
                return JsonResponse({
                    'vehicleId': vehicle.vehicleId,
                    'plate_number': vehicle.plate_number,
                    'image_url': vehicle.vehicleImage.url if vehicle.vehicleImage else None,
                })
            else:
                return JsonResponse({'error': 'No equipped vehicle'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'No userId provided'}, status=400)



def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicleId=vehicle_id)  # Using vehicleId for consistency
    
    if request.method == 'POST':
        # Update the vehicle fields from the POST data
        vehicle.vehicleManufacturer = request.POST.get('manufacturer', vehicle.vehicleManufacturer)
        vehicle.vehicleColor = request.POST.get('color', vehicle.vehicleColor)
        vehicle.vehicleType = request.POST.get('type', vehicle.vehicleType)

        vehicle.save()  # Save the changes to the vehicle

        # If it's an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'id': vehicle.id,
                'vehicleManufacturer': vehicle.vehicleManufacturer,
                'vehicleColor': vehicle.vehicleColor,
                'vehicleType': vehicle.vehicleType,
            })

        return redirect('sticker_management')  # For non-AJAX, redirect to the sticker management page
    
    # For GET requests (to handle the modal), pass vehicle to the context
    return render(request, 'sticker_management.html', {'vehicle': vehicle})


def delete_vehicle(request, vehicle_id):
    try:
        # Safely get the vehicle or raise a 404 if not found
        vehicle = get_object_or_404(Vehicle, vehicleId=vehicle_id)

        # Delete the vehicle
        vehicle.delete()

        # Check if the request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Vehicle deleted successfully.'})

        # For non-AJAX, redirect to the sticker management page
        return redirect('sticker_management')

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error deleting vehicle: {e}")

        # Handle AJAX requests with a JSON error response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Failed to delete vehicle.'}, status=400)

        # Handle non-AJAX requests with a general error message
        raise Http404("Vehicle could not be deleted.")

def renew_sticker(request, sticker_id):
    sticker = Sticker.objects.get(id=sticker_id)
    if request.method == 'POST':
        sticker.expiryDate = request.POST['expiry_date']
        sticker.save()
        return redirect('sticker_management')
    return render(request, 'renew_sticker.html', {'sticker': sticker})

def edit_sticker(request, sticker_id):
    sticker = get_object_or_404(Sticker, id=sticker_id)
    
    if request.method == 'POST':
        new_expiry_date = request.POST.get('new_expiry_date')
        
        if not new_expiry_date:
            return JsonResponse({'error': 'Expiry date is required'}, status=400)
        
        sticker.expiryDate = new_expiry_date
        sticker.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'id': sticker.id,
                'expiryDate': sticker.expiryDate,
            })
        
        return redirect('sticker_management')
    
    return render(request, 'edit_sticker.html', {'sticker': sticker})

def news(request):
    return render(request, 'news.html')



#######################################################################################################################################################

##### PARKING AREA #####

logger = logging.getLogger(__name__)


# Parking Area Views
def parking_area_list(request):
    parking_areas = ParkingArea.objects.all()
    return render(request, 'parking/parking_area_list.html', {'parking_areas': parking_areas})

def parking_area_create(request):
    if request.method == 'POST':
        form = ParkingAreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parking_area_list')
    else:
        form = ParkingAreaForm()
    return render(request, 'parking/parking_area_form.html', {'form': form})

def parking_area_update(request, pk):
    area = get_object_or_404(ParkingArea, pk=pk)
    if request.method == 'POST':
        form = ParkingAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('parking_area_list')
    else:
        form = ParkingAreaForm(instance=area)
    return render(request, 'parking/parking_area_form.html', {'form': form, 'area': area})

def parking_area_delete(request, pk):
    # Get the parking area by its primary key (pk)
    area = get_object_or_404(ParkingArea, pk=pk)

    # Check if the parking area has any associated parking lots
    if area.parking_lots.exists():
        # If there are parking lots, prevent deletion and show an error message
        messages.error(request, "Cannot delete this parking area because it has associated parking lots.")
        return redirect('parking_area_list')  # Redirect back to the list of parking areas

    # If there are no parking lots, proceed with deletion
    if request.method == 'POST':
        area.delete()
        messages.success(request, "Parking area deleted successfully.")
        return redirect('parking_area_list')  # Redirect after successful deletion

    # Render the confirmation page for deletion
    return render(request, 'api/parking_area_confirm_delete.html', {'parking_area': area})

# Parking Lot Views
def parking_lot_list(request, area_id):
    parking_area = get_object_or_404(ParkingArea, pk=area_id)
    parking_lots = parking_area.parking_lots.all()  # Get parking lots for the specific parking area
    print(parking_lots)  # Debugging step: check the list of parking lots
    return render(request, 'parking/parking_lot_list.html', {
        'parking_area': parking_area,
        'parking_lots': parking_lots
    })


def parking_lot_create(request, area_id):
    # Retrieve the parking area or return a 404 if not found
    parking_area = get_object_or_404(ParkingArea, pk=area_id)
    
    if request.method == 'POST':
        # Initialize the form with POST data and the parking area
        form = ParkingLotForm(request.POST, parking_area=parking_area)
        
        if form.is_valid():
            # Create a parking lot instance without saving it yet
            parking_lot = form.save(commit=False)
            parking_lot.parking_area = parking_area
            parking_lot.save()
            return redirect('parking_lot_list', area_id=area_id)
        else:
            # If the form is invalid, display the error message
            error_message = form.errors.get('parking_lot_number', None)
            return render(request, 'parking/parking_lot_form.html', {
                'form': form,
                'parking_area': parking_area,
                'error_message': error_message,
            })

    else:
        # Initialize the form without POST data
        form = ParkingLotForm(parking_area=parking_area)

    # Render the form with any existing error messages
    return render(request, 'parking/parking_lot_form.html', {
        'form': form,
        'parking_area': parking_area,
    })

def render_parking_lot_form(request, form, parking_area, error_message=None):
    """
    Helper function to render the parking lot form with additional context.
    """
    existing_lot_numbers = ParkingLot.objects.filter(parking_area=parking_area).values_list('parking_lot_number', flat=True)
    return render(request, 'parking/parking_lot_form.html', {
        'form': form,
        'parking_area': parking_area,
        'existing_lot_numbers': existing_lot_numbers,
        'error_message': error_message,
    })

def parking_lot_update(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    parking_area = lot.parking_area  # Get the associated parking area
    if request.method == 'POST':
        form = ParkingLotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            return redirect('parking_lot_list', area_id=parking_area.pk)
    else:
        form = ParkingLotForm(instance=lot)

    return render(request, 'parking/parking_lot_form.html', {
        'form': form,
        'lot': lot,
        'parking_area': parking_area,  # Pass the parking_area to the template
    })


from django.shortcuts import get_object_or_404, redirect, render
from .models import ParkingLot

def parking_lot_delete(request, pk):
    # Get the parking lot by its primary key (pk)
    lot = get_object_or_404(ParkingLot, pk=pk)

    # Store the parking area id, so we can redirect to the list of parking lots for this area after deletion
    parking_area = lot.parking_area  # The associated parking area of the lot

    if request.method == 'POST':
        lot.delete()  # Delete the parking lot
        return redirect('parking_lot_list', area_id=parking_area.pk)  # Redirect to parking lot list for the area

    # Render the delete confirmation page
    return render(request, 'parking/parking_lot_confirm_delete.html', {'parking_lot': lot})


# Toggle Parking Lot Status View
@require_POST
def toggle_parking_lot_status(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    lot.parking_lot_status = 'occupied' if lot.parking_lot_status == 'vacant' else 'vacant'
    lot.save()
    return redirect(reverse('parking_area_list'))  # Adjust if the redirect should be to a specific area
from django.http import JsonResponse
from .models import ParkingArea

# View to return parking areas with their parking lots as JSON
def parking_areas_with_lots(request):
    parking_areas = ParkingArea.objects.all()
    data = []
    for area in parking_areas:
        # You can decide whether to fetch all or only available lots
        lots = [{"id": lot.id, "parking_lot_number": lot.parking_lot_number, "is_available": lot.parking_lot_status == 'Available'} 
                for lot in area.parking_lots.all()]
        data.append({"id": area.parking_area_id, "parking_location": area.parking_location, "lots": lots})

    return JsonResponse({"parking_areas": data})

def available_lots(request, location_id):
    parking_area = get_object_or_404(ParkingArea, pk=location_id)
    available_parking_lots = parking_area.parking_lots.filter(parking_lot_status='Available')

    data = [{
        "id": lot.id,
        "parking_lot_number": lot.parking_lot_number
    } for lot in available_parking_lots]

    return JsonResponse({"available_lots": data})


# Set up logging
logger = logging.getLogger(__name__)

# Set up logging
logger = logging.getLogger(__name__)

def reservation(request):
    context1 = get_base_context(request)  # Base context with additional data
    if request.method == 'POST':
        # Ensure the user is logged in before allowing reservation
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User must be logged in to make a reservation"}, status=401)

        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Log the received data for debugging
        logger.info("Received reservation data: %s", data)

        # Create a ReservationForm instance using the parsed data
        form = ReservationForm(data)

        if form.is_valid():
            # Save the reservation but do not commit to the database yet
            reservation = form.save(commit=False)
            reservation.user = request.user  # Associate the logged-in user with the reservation

            # Get the parking lot associated with the reservation
            parking_lot = reservation.parking_lot

            # Check if the parking lot is available
            if parking_lot.parking_lot_status == 'Occupied':
                return JsonResponse({'error': 'The selected parking lot is already occupied.'}, status=400)

            # Save the reservation
            reservation.save()

            # After saving, mark the parking lot as "Occupied"
            parking_lot.parking_lot_status = 'Occupied'
            parking_lot.save()

            # Prepare the confirmation URL
            confirmation_url = reverse('reservation_confirmation', kwargs={'pk': reservation.pk})
            
            # Respond with a success message and the confirmation URL
            return JsonResponse({'success': True, 'confirmation_url': confirmation_url})

        else:
            # Log form errors and return them as part of the response
            logger.error(f"Form validation failed with errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        # For GET requests, render the reservation form
        form = ReservationForm()
        # Merge context1 with the new context containing the form
        context = {'form': form}
        context.update(context1)
        return render(request, 'parking/reservation.html', context)

    
    
def reservation_confirmation(request, pk):
    logger.info(f"Reservation Confirmation View Triggered with PK: {pk}")
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'parking/reservation_confirmation.html', {'reservation': reservation})

def get_parking_areas(request):
    # Get parking areas from the database
    parking_areas = ParkingArea.objects.all()
    # Return the parking areas in a JSON response
    return JsonResponse({'parking_areas': list(parking_areas.values())})

# View to get parking lots for a specific parking area

logger = logging.getLogger(__name__)





def get_parking_lots(request, area_id):
    try:
        # Retrieve the parking area by ID
        parking_area = ParkingArea.objects.get(parking_area_id=area_id)
        # Get all parking lots associated with this area
        parking_lots = ParkingLot.objects.filter(parking_area=parking_area)
        data = {
            "parking_lots": [
                {
                    "id": lot.parking_lot_id,
                    "parking_lot_number": lot.parking_lot_number,
                    "status": lot.parking_lot_status,
                    "user_id": lot.user.userId if lot.user else None
                } for lot in parking_lots
            ]
        }
        return JsonResponse(data)
    except ParkingArea.DoesNotExist:
        # If parking area not found, return an error message
        return JsonResponse({"error": "Parking area not found"}, status=404)
    

def parking_area1(request):
    # Get the base context
    context = get_base_context(request)
    
    # Get the extended context that includes vehicle_id
    context2 = get_base_context2(request)
    
    # Merge both context dictionaries
    context.update(context2)
    
    # Pass the combined context to the template
    return render(request, 'parking/area1.html', context)


def parking_area2(request):
    # Any necessary context data for Parking Area 2
    context = get_base_context(request)
    return render(request, 'parking/area2.html', context)

def parking_area3(request):
    # Any necessary context data for Parking Area 3
    context = get_base_context(request)
    return render(request, 'parking/area3.html', context)

def parking_area4(request):
    # Any necessary context data for Parking Area 4
    return render(request, 'parking/area4.html')    


def reservation_view(request, area_id):
    return render(request, 'area.html', {'area_id': area_id})

# POST CURRENT EQUIPPED VEHICLE IN THE PARKING LOT 

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def reserve_parking(request):
    try:
        data = json.loads(request.body)
        lot_id = data.get('lot_id')  # lot_id corresponds to parking_lot_id
        user_id = data.get('user_id')
        vehicle_id = data.get('vehicle_id')

        # Fetch user and vehicle using proper field names
        user = User.objects.get(userId=user_id)
        vehicle = Vehicle.objects.get(vehicleId=vehicle_id)
        
        # Fetch parking lot using the correct field name 'parking_lot_id'
        parking_lot = ParkingLot.objects.get(parking_lot_id=lot_id)  # Use parking_lot_id here

        

        # Now proceed with reserving the parking lot
        if parking_lot.parking_lot_status == 'Available':
            parking_lot.parking_lot_status = 'Occupied'
            parking_lot.user = user  # Associate the parking lot with the user who reserved it
            parking_lot.vehicle = vehicle  # Assign the vehicle to the parking lot
            parking_lot.save()

            # Mark vehicle as equipped (if not already done)
            vehicle.is_equipped = True
            vehicle.save()

            return JsonResponse({'status': 'success', 'message': 'Parking lot reserved successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Parking lot is already occupied.'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
    except Vehicle.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vehicle not found for this user.'}, status=404)
    except ParkingLot.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Parking lot not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

    ### UNPARK VEHICLE

@csrf_exempt
def unpark_vehicle(request):
    if request.method == 'POST':
        try:
            # Parse JSON payload from the request
            import json
            data = json.loads(request.body)
            lot_id = data.get('lot_id')

            # Validate input
            if not lot_id:
                return JsonResponse({"status": "error", "message": "Parking lot ID is required."}, status=400)

            # Fetch the parking lot
            lot = ParkingLot.objects.get(pk=lot_id)

            # Update the parking lot status to 'Available'
            lot.parking_lot_status = "Available"
            lot.user = None
            lot.vehicle = None
            lot.save()

            return JsonResponse({"status": "success", "message": "Parking lot has been successfully updated to 'Available'."})
        except ParkingLot.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Parking lot not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method. Only POST is allowed."}, status=405)












