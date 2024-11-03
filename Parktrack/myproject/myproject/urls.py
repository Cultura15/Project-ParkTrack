"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from parking.views import (
    home,  # Add this import for the home view
    vehicle_list, vehicle_create, vehicle_update, vehicle_delete,
    sticker_list, sticker_create, sticker_update, sticker_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/create/', vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:pk>/', vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:pk>/', vehicle_delete, name='vehicle_delete'),
    path('stickers/', sticker_list, name='sticker_list'),
    path('stickers/create/', sticker_create, name='sticker_create'),
    path('stickers/update/<int:pk>/', sticker_update, name='sticker_update'),
    path('stickers/delete/<int:pk>/', sticker_delete, name='sticker_delete'),
]
