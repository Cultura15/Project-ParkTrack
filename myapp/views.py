from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicle, Sticker
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json

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
    # Assuming the user is logged in and we can access the user through the request
    user = request.user  # Get the logged-in user
    if user.is_authenticated:
        user_name = f"{user.first_name} {user.last_name}"  # Concatenate first and last name
        user_fname = {user.last_name}
        user_role = user.groups.first().name if user.groups.exists() else 'Guest'  # Assume role is from a group, or 'Guest'
    else:
        user_name = "Guest"
        user_role = "Guest"
        user_fname = "Guest"
    
    return render(request, 'menu.html', {'user_name': user_name, 'user_role': user_role})


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
            user.accountType = request.POST.get('accountType', user.accountType)
            user.save()

            return JsonResponse({'success': 'User updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        

def parkingMap(request):
    return render(request, 'parkingMap.html')
        




##############################################################################################################################################

##### ARTEZUELA #####

def sticker_management(request):
    stickers = Sticker.objects.all()  # Retrieve all stickers for management
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
        return redirect('sticker_management')
    return render(request, 'register_vehicle.html')

def edit_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if request.method == 'POST':
        vehicle.vehicleManufacturer = request.POST['manufacturer']
        vehicle.vehicleColor = request.POST['color']
        vehicle.vehicleType = request.POST['type']
        vehicle.save()
        return redirect('sticker_management')
    return render(request, 'edit_vehicle.html', {'vehicle': vehicle})

def delete_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return redirect('sticker_management')

def renew_sticker(request, sticker_id):
    sticker = Sticker.objects.get(id=sticker_id)
    if request.method == 'POST':
        sticker.expiryDate = request.POST['expiry_date']
        sticker.save()
        return redirect('sticker_management')
    return render(request, 'renew_sticker.html', {'sticker': sticker})


#######################################################################################################################################################

##### DESTURA #####






