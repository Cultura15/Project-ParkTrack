from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json

def home(request):
    return render(request, 'home.html')

# Registration view NICE
@csrf_exempt
def register(request):
    if request.method == 'GET':
        # Serve the registration HTML page
        return render(request, 'register.html')

    if request.method == 'POST':
        # Check the content type of the request
        if request.content_type == 'application/json':
            # If JSON, load the data
            data = json.loads(request.body)
        else:
            # Otherwise, assume it's form data
            data = request.POST

        try:
            user = User(
                fname=data.get('fname'),
                lname=data.get('lname'),
                email=data.get('email'),
                gender=data.get('gender'),
                address=data.get('address'),
                contactNo=data.get('contactNo'),
                accountType=data.get('accountType'),
                username=data.get('email'),  # Use email as username
                password=make_password(data.get('password'))  # Hash the password
            )
            user.save()
            return JsonResponse({'message': 'Registration successful!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# Login view NICE
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load JSON data from the request
            email = data.get('email')
            password = data.get('password')

            # Attempt to authenticate the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Return the error for debugging
    else:  # Handle GET requests
        return render(request, 'login.html')
    
# MENU
def menu_view(request):
    return render(request, 'menu.html')

# GET all users    
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all().values(  # Use values() to specify the fields to include
            'fname', 'lname', 'email', 'contactNo', 'address', 'password', 'accountType'
        )
        return JsonResponse(list(users), safe=False, status=200)  # Return users as a JSON response
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')  



