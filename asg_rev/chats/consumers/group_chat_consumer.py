import json
import base64
import struct
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.core.files.base import ContentFile
from io import BytesIO
from django.db import close_old_connections
from workspaces.models import Channel, ChannelRole
from chats.models.message import GroupMessage
from django.contrib.auth.models import AnonymousUser

class GroupChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"group_chat_{self.room_name}"

        user = self.scope["user"]
        try:
            workspace_id, category_id, channel_id = self.room_name.split("_")
            self.channel = await sync_to_async(get_object_or_404)(Channel, id=channel_id)
            
            if not await self.is_user_in_channel(user):
                raise DenyConnection("User is not a member of this channel.")
        except ValueError:
            raise DenyConnection("Invalid room_name format.")
        except Channel.DoesNotExist:
            raise DenyConnection("Channel does not exist.")
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Check if the message is binary data
        if text_data[0] == 'B':
            await self.handle_file_upload(text_data[1:])
        else:
            await self.handle_text_message(text_data)

    async def handle_file_upload(self, data):
        """Handles file uploads sent as raw binary data."""
        # Extract header and binary data (e.g., file data)
        header, file_data = self.extract_file_header_and_data(data)

        # Save the file to the server (for example, saving to the database)
        await self.save_file(header['file_name'], file_data)

        # Broadcast the file to all connected clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_file",
                "file_name": header['file_name'],
                "file_data": file_data,
                "sender": self.scope["user"].username
            }
        )

    def extract_file_header_and_data(self, data):
        """Extracts the header (file name, length) and the binary file data."""
        # Assuming the first 4 bytes contain the length of the file name as an integer
        header_length = struct.unpack("!I", data[:4])[0]
        file_name = data[4:4 + header_length].decode('utf-8')
        binary_data = data[4 + header_length:]

        return {'file_name': file_name}, binary_data

    async def save_file(self, file_name, file_data):
        """Saves the file to the database."""
        file_content = base64.b64decode(file_data)

        content_file = ContentFile(file_content, name=file_name)

        # Save the file in the model (or wherever you want to store it)
        # Example:
        # GroupMessage.objects.create(
        #     sender=self.scope["user"],
        #     text_content="File received",
        #     file=content_file,
        #     channel=self.channel
        # )

    async def handle_text_message(self, text_data):
        """Handles the regular text message."""
        data = json.loads(text_data)
        content = data.get('message')

        if content:
            await self.save_message(content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'sender': self.scope["user"].username,
                        'content': content,
                    }
                }
            )

    async def save_message(self, content):
        """Saves the message to the database asynchronously."""
        user = self.scope["user"]
        await database_sync_to_async(GroupMessage.objects.create)(
            sender=user,
            text_content=content,
            channel=self.channel
        )

    async def chat_message(self, event):
        """Sends the chat message to the WebSocket."""
        await self.send(text_data=json.dumps(event['message']))

    async def chat_file(self, event):
        """Sends the file data to the WebSocket."""
        await self.send(text_data=json.dumps({
            "file_name": event["file_name"],
            "file_data": event["file_data"],
            "sender": event["sender"]
        }))

    @sync_to_async
    def is_user_in_channel(self, user):
        return ChannelRole.objects.filter(channel=self.channel, user=user).exists()
