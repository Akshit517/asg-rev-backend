from django.urls import path

from chats.consumers.group_chat_consumer import GroupChatConsumer

websocket_urlpatterns = [
    path("ws/group-chat/<room_name>/", GroupChatConsumer.as_asgi()),
]