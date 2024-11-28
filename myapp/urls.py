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
    path('news/', views.news, name='news'), 
    path('trymap/', views.map_view, name='map_view'),
   
   
 
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

    # destura

    path('parking-areas/', views.parking_area_list, name='parking_area_list'),
    path('parking-areas/add/', views.parking_area_create, name='parking_area_create'),
    path('parking-areas/edit/<int:pk>/', views.parking_area_update, name='parking_area_update'),
    path('parking-areas/delete/<int:pk>/', views.parking_area_delete, name='parking_area_delete'),
    
    path('parking-lots/<int:area_id>/', views.parking_lot_list, name='parking_lot_list'),
    path('parking-lots/add/<int:area_id>/', views.parking_lot_create, name='parking_lot_create'),  # Updated
    path('parking-lots/edit/<int:pk>/', views.parking_lot_update, name='parking_lot_update'),
    path('parking-lots/delete/<int:pk>/', views.parking_lot_delete, name='parking_lot_delete'),
    path('parking-lot/<int:pk>/toggle-status/', views.toggle_parking_lot_status, name='parking_lot_toggle_status'),
    path('api/available-lots/<int:location_id>/', views.available_lots, name='available_lots'),
    path('reservation/', views.reservation, name='reservation'),
    path('parking-areas-with-lots/', views.parking_areas_with_lots, name='parking_areas_with_lots'),
    path('get-parking-areas/', views.get_parking_areas, name='get_parking_areas'),
    path('get-parking-lots/<int:area_id>/', views.get_parking_lots, name='get_parking_lots'),

    path('area1/', views.parking_area1, name='parking_area1'),
    path('area2/', views.parking_area2, name='parking_area2'),
    path('area3/', views.parking_area3, name='parking_area3'),
    path('area4/', views.parking_area4, name='parking_area4'),


    
]
