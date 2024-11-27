from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('users/', views.user_list, name='user_list'),  # List all users
    path('users/<int:user_id>/', views.user_detail, name='user_detail'), 
    path('update_user/', views.update_user, name='update_user'),
    path('get_user_details/', views.get_user_details, name='get_user_details'), 
    path('parkingMap/', views.parkingMap, name='parkingMap'), 
    path('aboutUs/', views.aboutUs, name='aboutUs'), 
    path('parkReserve/', views.parkReserve, name='parkReserve'), 
    path('accountSettings/', views.accountSettings, name='accountSettings'), 
   
   
 
 

    # artezuela
    path('sticker_management/', views.sticker, name='sticker'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'),
    path('equip_vehicle/', views.equip_vehicle, name='equip_vehicle'),
    path('get_equipped_vehicle/', views.get_equipped_vehicle, name='get_equipped_vehicle'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_details, name='vehicle_details'),
    path('edit_vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('renew_sticker/<int:sticker_id>/', views.renew_sticker, name='renew_sticker'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
    
]
