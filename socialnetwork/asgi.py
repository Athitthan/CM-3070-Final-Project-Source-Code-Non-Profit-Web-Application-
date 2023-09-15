"""
ASGI config for socialnetwork project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from mysocialapp.routing import websocket_urlpatterns



# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork.settings')

# Get the ASGI application for Django
django_asgi_app = get_asgi_application()

# Import WebSocket URL patterns from your application's routing module
import mysocialapp.routing

# Create the ASGI application, handling both HTTP and WebSocket protocols
application=ProtocolTypeRouter({
    "http":django_asgi_app, # Handle HTTP requests using Django ASGI application
    "websocket":AllowedHostsOriginValidator( # Enforce allowed hosts for WebSocket connections
        AuthMiddlewareStack(URLRouter(mysocialapp.routing.websocket_urlpatterns))# Authenticate WebSocket connections
    ),
    
})
