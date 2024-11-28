import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Ensure Django is set up before accessing any Django models or other parts
django.setup()

# Now you can import routing and consumers after django.setup()
from myapp import routing  # Import your WebSocket routing module

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Define your WebSocket routes here
        )
    ),
})

