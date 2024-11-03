# myproject/parking/urls.py
from django.urls import path
from .views import vehicle_list, vehicle_create, vehicle_update, vehicle_delete
from .views import sticker_list, sticker_create, sticker_update, sticker_delete
from .views import home

urlpatterns = [
    path('', home, name='home'),  # Add this line for the home page
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/create/', vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:pk>/', vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:pk>/', vehicle_delete, name='vehicle_delete'),
    path('stickers/', sticker_list, name='sticker_list'),
    path('stickers/create/', sticker_create, name='sticker_create'),
    path('stickers/update/<int:pk>/', sticker_update, name='sticker_update'),
    path('stickers/delete/<int:pk>/', sticker_delete, name='sticker_delete'),
]
