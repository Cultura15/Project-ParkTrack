from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('users/', views.user_list, name='user_list'),  # List all users
    path('users/<int:user_id>/', views.user_detail, name='user_detail'), 
    path('update_user/', views.update_user, name='update_user'),

    # artezuela
    path('sticker_management/', views.sticker, name='sticker'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'),
    path('edit_vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('renew_sticker/<int:sticker_id>/', views.renew_sticker, name='renew_sticker'),
    path('sticker_management/', views.sticker_management, name='sticker_management'),
    
]