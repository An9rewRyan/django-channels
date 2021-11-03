import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from chat.views import make_comment
import datetime
from django.contrib.auth.models import User
from chat.models import Comment, Game
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"]

        data = await self.make_comment(message['message'], message['game_id'], message['comment_status'], username)
        print(data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    @database_sync_to_async
    def make_comment(self, text, game_id, comment_status, user):

        now = datetime.datetime.now()
        game = Game.objects.get(pk = game_id)
        user = User.objects.get(username=user)

        if comment_status == 'solo':
            comment = Comment(texts = text, game = game, user = user, pub_date = now)
            comment.save()
            comment = Comment.objects.get(texts = text, game = game, user = user, pub_date = now)
            dict_ = {'id': comment.pk,
                    'user':user.username,
                    'text': text,
                    'comment_status':comment_status,
                    'pub_date':str(now)}
            return dict_ 

        else:
            parent_comment = Comment.objects.get(pk = comment_status)
            parent_user = User.objects.get(username = parent_comment.user)
            
            comment = Comment(texts = text, game = game, user = user, pub_date = now, reply_to = parent_comment, replied_user_name = parent_user.username )
            comment.save()
            
            comment = Comment.objects.get(texts = text, game = game, user = user, pub_date = now)

            dict_ = {'id': comment.pk,
                    'user':user.username,
                    'text': text,
                    'reply_to_id': parent_comment.pk,
                    'comment_status':comment_status,
                    'pub_date':str(now),
                    'reply_to_user':  parent_user.username}
            return dict_

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))