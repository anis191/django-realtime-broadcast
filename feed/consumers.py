import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('feed', self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('feed', self.channel_name)
    
    async def new_post(self, event):
        await self.send(text_data=json.dumps({
            'content' : event['content'],
            # 'username' : event['username', 'User'],
            'username': event.get('username', 'User'),
            'post_type' : event.get("post_type", "normal"),
            "rank" : event.get("rank")
        }))