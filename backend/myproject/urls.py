from django.contrib import admin
from django.urls import path, include
from myapp.views import home, menu_view, accountSettings, base_view1, parkReserve, upload_profile_picture, delete_profile_picture
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # This includes URLs from `myapp`
    path('', home, name='home'), 
    path('menu/', menu_view, name='menu'), 
    path('base/', base_view1, name='base'), 
    path('accountSettings/', accountSettings, name='accountSettings'),
    path('parkReserve/', parkReserve, name='parkReserve'), 
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'), 
    path('delete-profile-picture/', delete_profile_picture, name='delete_profile_picture'),

   

  
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

