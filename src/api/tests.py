# src/api/tests.py
from django.test import TestCase
from api.models import Room, Booking

class BookingAPITest(TestCase):
    def test_create_room_and_booking(self):
        r = Room.objects.create(description="t", price=100)
        resp = self.client.post('/bookings/create', data={
            'room_id': r.id,
            'date_start': '2023-01-01',
            'date_end': '2023-01-03'
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn('booking_id', body)
        b_id = body['booking_id']
        b = Booking.objects.get(id=b_id)
        self.assertEqual(b.room.id, r.id)

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
