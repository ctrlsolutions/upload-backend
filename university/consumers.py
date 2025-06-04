import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CollegeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("college_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("college_updates", self.channel_name)

    async def receive(self, text_data):
        # Not needed for now; we're only sending from server
        pass

    async def college_added(self, event):
        await self.send(text_data=json.dumps({
            "type": "college_added",
            "data": event["data"],
        }))


class DepartmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("departments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("departments", self.channel_name)

    async def department_created(self, event):
        await self.send(text_data=json.dumps(event["data"]))
