# parking/routing.py

from django.urls import re_path
from myapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/reservation_area/(?P<area_id>\d+)/$', consumers.ReservationConsumer.as_asgi()),
]
