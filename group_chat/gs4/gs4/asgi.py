import os
from django.urls import path
from app.consummers import MySyncConsumer, MyAsyncConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import app.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gs4.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':  AuthMiddlewareStack(URLRouter( [
    path('ws/sc/<str:groupkanme>/', MySyncConsumer.as_asgi()),
    path('ws/ac/', MyAsyncConsumer.as_asgi()),
    ]
    ))
})