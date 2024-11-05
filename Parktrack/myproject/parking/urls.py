from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'),
    path('edit_vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('renew_sticker/<int:sticker_id>/', views.renew_sticker, name='renew_sticker'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
]