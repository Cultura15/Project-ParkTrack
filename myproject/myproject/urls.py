from django.contrib import admin
from django.urls import path, include
from myapp.views import home, menu_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # This includes URLs from `myapp`
    path('', home, name='home'), 
    path('menu/', menu_view, name='menu'),
]

