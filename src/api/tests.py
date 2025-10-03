# src/api/tests.py
from django.test import TestCase

from api.models import Booking, Room


class BookingAPITest(TestCase):
    def test_create_room_and_booking(self):
        # Создаём комнату через API
        resp = self.client.post('/rooms/create', data={
            'description': 'Test room',
            'price': 100.00
        })
        self.assertEqual(resp.status_code, 200)
        room_data = resp.json()
        room_id = room_data['room_id']

        # Создаём бронирование напрямую через модель
        from datetime import date
        b = Booking.objects.create(
            room_id=room_id,
            date_start=date(2023, 1, 1),
            date_end=date(2023, 1, 3)
        )
        self.assertEqual(b.room.id, room_id)

    def test_overlapping_booking_blocked(self):
        r = Room.objects.create(description="t2", price=100)
        _existing = Booking.objects.create(room=r, date_start='2023-01-10', date_end='2023-01-15')
        resp = self.client.post('/bookings/create', data={
            'room_id': r.id,
            'date_start': '2023-01-12',
            'date_end': '2023-01-13'
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
