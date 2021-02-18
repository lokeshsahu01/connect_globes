from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from folder_structure.consumer import EchoConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", EchoConsumer),
    ])
})
