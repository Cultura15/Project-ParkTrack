from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

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
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)