from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicle, Sticker
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404,  HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt, csrf_protect  
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json, logging, requests

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

def base_view(request):
    user = request.user  # Get the logged-in user

    if user.is_authenticated:
        # Fetch user details
        user_name = f"{user.first_name} {user.last_name}"  # Combine first and last name
        user_fname = user.first_name
        user_role = user.groups.first().name if user.groups.exists() else 'Guest'  # Role based on groups, fallback to 'Guest'

        # Call the get_equipped_vehicle API to get the vehicle details
        try:
            response = requests.get(f'http://127.0.0.1:8000/api/get_equipped_vehicle/?userId={user.id}')
            vehicle_info = response.json()
            if 'error' not in vehicle_info:
                vehicle_info = {
                    "manufacturer": vehicle_info.get('manufacturer', 'N/A'),
                    "type": vehicle_info.get('type', 'N/A'),
                    "color": vehicle_info.get('color', 'N/A'),
                    "plate_number": vehicle_info.get('plate_number', 'N/A'),
                    "image_url": vehicle_info.get('image_url', '/static/default-vehicle.png')
                }
            else:
                vehicle_info = {
                    "manufacturer": "None",
                    "type": "N/A",
                    "color": "N/A",
                    "plate_number": "N/A",
                    "image_url": "/static/default-vehicle.png"
                }
        except requests.RequestException:
            vehicle_info = {
                "manufacturer": "None",
                "type": "N/A",
                "color": "N/A",
                "plate_number": "N/A",
                "image_url": "/static/default-vehicle.png"
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
            "image_url": "/static/default-vehicle.png"
        }

    # Render the menu template with user and vehicle information
    return render(request, 'base.html', {
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
        

def parkingMap(request):
    return render(request, 'parkingMap.html')

def aboutUs(request):
    return render(request, 'aboutus.html')

def parkReserve(request):
    return render(request, 'parkreserve.html')

def accountSettings(request):
    return render(request, 'account.html')
        




##############################################################################################################################################

##### ARTEZUELA #####

def sticker_management(request):
    try:
        stickers = Sticker.objects.all()
    except Exception as e:
        logging.error(f"Error retrieving stickers: {e}")
        return HttpResponseServerError("Something went wrong while fetching stickers.")
    return render(request, 'sticker_management.html', {'stickers': stickers})


def sticker(request):
    vehicles = Vehicle.objects.all()
    stickers = Sticker.objects.all()
    return render(request, 'sticker.html', {
        'vehicles': vehicles,
        'stickers': stickers,
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


#######################################################################################################################################################

##### DESTURA #####






