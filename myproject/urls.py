from django.contrib import admin
from django.urls import path, include
from myapp.views import home, menu_view
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # This includes URLs from `myapp`
    path('', home, name='home'), 
    path('menu/', menu_view, name='menu'), 
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

