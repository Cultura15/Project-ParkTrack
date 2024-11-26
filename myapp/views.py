from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicle, Sticker
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404,  HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json, logging


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
            "plate_number": "ABC-1234" if vehicle else "N/A"  # Placeholder plate info
        }
    else:
        user_name = "Guest"
        user_fname = "Guest"
        user_role = "Guest"
        vehicle_info = {
            "manufacturer": "None",
            "type": "N/A",
            "color": "N/A",
            "plate_number": "N/A"
        }

    # Render the menu template with user and vehicle information
    return render(request, 'menu.html', {
        'user_name': user_name,
        'user_role': user_role,
        'user_fname': user_fname,
        'vehicle_info': vehicle_info,
    })

#api/base
def base_view(request):
    if request.user.is_authenticated:
        # Get user and associated vehicle info
        user = request.user
        vehicle = getattr(user, 'vehicle', None)
        
        vehicle_info = {
            "manufacturer": vehicle.vehicleManufacturer if vehicle else "None",
            "type": vehicle.vehicleType if vehicle else "N/A",
            "color": vehicle.vehicleColor if vehicle else "N/A",
            "plate_number": "ABC-1234" if vehicle else "N/A"  # Placeholder plate info
        }
    else:
        # Return default info for guests
        vehicle_info = {
            "manufacturer": "None",
            "type": "N/A",
            "color": "N/A",
            "plate_number": "N/A"
        }

    # Return the vehicle info as JSON
    return JsonResponse(vehicle_info)



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

            # Handle optional vehicle image
            vehicle_image = request.FILES.get('vehicleImage')

            # Create the vehicle
            vehicle = Vehicle(
                vehicleManufacturer=request.POST['manufacturer'],
                vehicleColor=request.POST['color'],
                vehicleType=request.POST['type'],
                vehicleImage=vehicle_image,
            )
            vehicle.save()

            # Associate the user with the vehicle
            user.vehicle = vehicle
            user.save()

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
                    'id': vehicle.id,
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






