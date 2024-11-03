from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     path('menu/', views.menu_view, name='menu'),  
    path('getUsers/', views.get_all_users, name='getUsers'),
    path('dashboard/', views.dashboard, name='dashboard'),  # placeholder for a dashboard view
]
