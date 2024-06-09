import json
import uuid
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from app.models import Message, ActorProfile

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"chat_{self.room_name}"

        try:
            user_profile = User.objects.get(id=self.user_id)
            self.username = user_profile.username
        except ActorProfile.DoesNotExist:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(json.dumps({
            "from": "System",
            "to": self.username,
            "messageBody": "Connection established"
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_body = text_data_json['messageBody']
        receiver_username = text_data_json['receiver']
        
        # Retrieve sender user object
        sender_user = User.objects.get(username=self.username)
        sender_id = sender_user.id
        
        # Retrieve receiver user object
        receiver_user = User.objects.get(username=receiver_username)
        receiver_id = receiver_user.id
        
        # Save the message to the database
        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_text=message_body
        )
        
        # Send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'chat_message',
                'sender': self.username,
                'receiver': receiver_username,
                'messageBody': message_body,
                'sendAt': message.sent_at.isoformat()
            }
        )

    def chat_message(self, event):
        sender = event['sender']
        receiver = event['receiver']
        message_body = event['messageBody']
        send_at = event['sendAt']
        
        message_data = {
            "id": str(uuid.uuid4()),  # Generate a unique ID for the message
            "sender": sender,
            "receiver": receiver,
            "messageBody": message_body,
            "sendAt": send_at
        }

        # Check if the message is intended for the current user
        if receiver == self.username:
            self.send(text_data=json.dumps(message_data))
