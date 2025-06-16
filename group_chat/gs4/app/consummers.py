from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Group, Chat

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected...', event)
        print("channels Layer...", self.channel_layer)
        print("channels name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkanme']
        print("Group Name.....", self.group_name )
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type':'websocket.accept',
        })
    
    def websocket_receive(self, event):
        print('message received from client', event)
        print('message received from client', event['text'])
        print('type of message', type(event['text']))
        coool = event['text']
        
        if not coool:
            print('Received empty message')
            return

        try:
            data = json.loads(coool)
        except json.JSONDecodeError as e:
            print('JSON decode error:', e)
            return

        print("data....", data)

        
        if 'msg' not in data:
            print('Message does not contain "msg" key')
            return

        print('chat message', data['msg'])
        print(self.scope['user'])
        # Find group object
        group = Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content=data['msg'],
                group=group
            )
            chat.save()
            data['user'] = self.scope['user'].username
            print("complate data", data)
            print('Type of data ', type(data))
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type':'websocket.send',
                'text': json.dumps({'msg':"login Required"})
            })


    def chat_message(self, event):
        print('Event...', event)
        print('Actual data...', event['message'])
        print('Type of data...', type(event['message']))
        self.send({
            'type':'websocket.send',
            'text':event['message'],
        })
        
                
    def websocket_disconnect(self, event):
        print('websocket disconected,,,', event)
        print("channels Layer...", self.channel_layer)
        print("channels name...", self.channel_name)
        self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()
    
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocket connected...', event)
        await self.send({
            'type':"websocket.accept",
        })
    
    async def websocket_receive(self, event):
        print('message recived from client', event)
        print('message recived from client', event['text'])
    
    async def websocket_disconnect(self, event):
        print('websocket disconected,,,', event)
        raise StopConsumer()
    
