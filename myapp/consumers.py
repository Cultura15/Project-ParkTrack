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
        # Parse the incoming message data
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'reserve':
            # Handle reservation logic
            lot_id = data['lot_id']
            lot_number = data['lot_number']
            user_id = data['user']
            entry_date = data['entry_date']
            entry_time = data['entry_time']
            exit_date = data['exit_date']
            exit_time = data['exit_time']

            try:
                # Fetch the parking lot and user
                lot = ParkingLot.objects.get(id=lot_id)
            except ParkingLot.DoesNotExist:
                return await self.send(text_data=json.dumps({
                    'error': 'Parking lot not found'
                }))

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return await self.send(text_data=json.dumps({
                    'error': 'User not found'
                }))

            if lot.parking_lot_status == 'Occupied':
                return await self.send(text_data=json.dumps({
                    'error': 'Parking lot is already occupied'
                }))

            # Create a reservation
            reservation = Reservation.objects.create(
                parking_area=lot.parking_area,
                parking_lot=lot,
                user=user,
                entry_date=entry_date,
                entry_time=entry_time,
                exit_date=exit_date,
                exit_time=exit_time
            )

            # Update the parking lot status
            lot.parking_lot_status = 'Occupied'
            lot.save()

            # Send reservation confirmation to the WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reservation_update',
                    'lot_id': lot_id,
                    'lot_number': lot_number,
                    'status': 'Occupied'
                }
            )

    # Receive a reservation update to send to WebSocket clients
    async def reservation_update(self, event):
        lot_id = event['lot_id']
        lot_number = event['lot_number']
        status = event['status']

        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'lot_id': lot_id,
            'lot_number': lot_number,
            'status': status
        }))
