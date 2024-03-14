import asyncio
from django.utils import timezone
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL route parameters
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Accept the WebSocket connection
        await self.accept()

        # ---I WROTE THIS CODE---

        # Load chat history asynchronously from the database
        chat_history = await self.get_chat_history()

        # Send chat history to the connected user
        await self.send_chat_history(chat_history)
        # ---END OF CODE THAT I WROTE---

        # Add the user to the group for the chat room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print("Connected")

    async def disconnect(self, close_code):
        print("Disconnected")

        # Remove the user from the chat room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        receiver = text_data_json["receiver"]
        sender = self.scope["user"].username  # Assuming you have authenticated users

        # ---I WROTE THIS CODE---
        # Save the message to the database asynchronously
        if message != "":
           await self.save_message_to_db(sender, message, receiver)
        # ---END OF CODE THAT I WROTE---

        # mark message from sender as read
        await self.mark_messages_as_read(receiver)

        # Send the received message to all users in the chat room
        if message != "":
           await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send the received chat message to the WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                }
            )
        )

    # ---I WROTE THIS CODE---
    # Decorate the method to make it asynchronous
    @database_sync_to_async
    def get_chat_history(self):
        return ChatMessage.objects.filter(room_name=self.room_name).order_by(
            "timestamp"
        )

    # Decorate the method to make it asynchronous
    @database_sync_to_async
    def save_message_to_db(self, sender, message, receiver):
        ChatMessage.objects.create(
            room_name=self.room_name,
            sender=sender,
            message=message,
            receiver=receiver,
        )

    # Decorate the method to make it asynchronous
    @database_sync_to_async
    def send_chat_history(self, chat_history):
        history_data = [
            {
                "sender": message.sender,
                "message": message.message,
                "timestamp": message.timestamp.astimezone(
                    timezone.get_current_timezone()
                ).strftime("%d-%m-%Y %H:%M"),
            }
            for message in chat_history
        ]

        # Send the chat history data to the WebSocket
        async def send_json_data():
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_history",
                        "history_data": history_data,
                    }
                )
            )

        async_to_sync(send_json_data)()

        # ---END OF CODE THAT I WROTE---

    @database_sync_to_async
    def mark_messages_as_read(self, receiver):
        ChatMessage.objects.filter(room_name=self.room_name, sender=receiver).update(
            is_read=True
        )
