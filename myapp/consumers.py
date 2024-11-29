import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ParkingArea, ParkingLot, Reservation
from django.contrib.auth.models import User

class ReservationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the parking area ID from the URL
        self.area_id = self.scope['url_route']['kwargs']['area_id']
        self.room_group_name = f"reservation_area_{self.area_id}"

        # Join the WebSocket group for this parking area
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        lot_id = data['lot_id']
        lot_number = data['lot_number']
        user_id = data['user']

        try:
            lot = ParkingLot.objects.get(id=lot_id)
        except ParkingLot.DoesNotExist:
            return await self.send(text_data=json.dumps({'error': 'Parking lot not found'}))

        if action == "reserve":
            # Reserve the parking lot
            if lot.parking_lot_status == "Occupied":
                return await self.send(text_data=json.dumps({'error': 'Parking lot is already occupied'}))
            
            lot.parking_lot_status = "Occupied"
            lot.save()

            # Notify all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reservation_update',
                    'lot_id': lot_id,
                    'lot_number': lot_number,
                    'status': "Occupied",
                    'user_id': user_id
                }
            )
        elif action == "release":
            # Release the parking lot
            lot.parking_lot_status = "Available"
            lot.save()

            # Notify all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reservation_update',
                    'lot_id': lot_id,
                    'lot_number': lot_number,
                    'status': "Available",
                    'user_id': None
                }
            )


    # Receive a reservation update to send to WebSocket clients
    async def reservation_update(self, event):
        await self.send(text_data=json.dumps({
            'lot_id': event['lot_id'],
            'lot_number': event['lot_number'],
            'status': event['status'],
            'user_id': event.get('user_id')  # Send user info for personalized updates
        }))

