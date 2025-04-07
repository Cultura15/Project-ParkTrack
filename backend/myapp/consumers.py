import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ParkingArea, ParkingLot, Reservation
from django.contrib.auth.models import User

class ReservationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.area_id = self.scope['url_route']['kwargs']['area_id']
        self.room_group_name = f"reservation_{self.area_id}"

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
        data = json.loads(text_data)
        lot_id = data.get('lot_id')
        user_id = data.get('user_id')
        vehicle_id = data.get('vehicle_id')

        # Log the values to check if they are being received correctly
        print(f"Received data: lot_id={lot_id}, user_id={user_id}, vehicle_id={vehicle_id}")

        # Proceed with the rest of the code
        if lot_id is None:
            print("Error: 'lot_id' is None")
            return  # Handle the error appropriately

        # Get the parking lot and update the status
        parking_lot = ParkingLot.objects.get(parking_lot_id=lot_id)
        parking_lot.user_id = user_id
        parking_lot.vehicle_id = vehicle_id
        parking_lot.parking_lot_status = 'Occupied'
        parking_lot.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'parking_lot_update',
                'lot_id': lot_id,
                'user_id': user_id,
                'vehicle_id': vehicle_id,
                'status': 'Occupied'
            }
        )


 