# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('parking-areas/', views.parking_area_list, name='parking_area_list'),
    path('parking-areas/add/', views.parking_area_create, name='parking_area_create'),
    path('parking-areas/edit/<int:pk>/', views.parking_area_update, name='parking_area_update'),
    path('parking-areas/delete/<int:pk>/', views.parking_area_delete, name='parking_area_delete'),
    
    path('parking-lots/', views.parking_lot_list, name='parking_lot_list'),
    path('parking-lots/add/<int:area_id>/', views.parking_lot_create, name='parking_lot_create'),  # Updated
    path('parking-lots/edit/<int:pk>/', views.parking_lot_update, name='parking_lot_update'),
    path('parking-lots/delete/<int:pk>/', views.parking_lot_delete, name='parking_lot_delete'),
    path('parking-lot/<int:pk>/toggle-status/', views.toggle_parking_lot_status, name='parking_lot_toggle_status'),
]
