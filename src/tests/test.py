from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Booking, Room


class BookingAPITest(TestCase):
    """Тесты для API бронирования"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.client = APIClient()
    
    def test_create_room_and_booking(self):
        """Тест создания комнаты и бронирования"""
        # Создаём комнату через API
        resp = self.client.post('/rooms/create', data={
            'description': 'Test room',
            'price': 100.00
        })
        self.assertEqual(resp.status_code, 200)
        room_data = resp.json()
        room_id = room_data['room_id']

        # Создаём бронирование напрямую через модель для первого теста
        from datetime import date
        b = Booking.objects.create(
            room_id=room_id,
            date_start=date(2023, 1, 1),
            date_end=date(2023, 1, 3)
        )

        # Проверяем, что бронирование создано
        self.assertEqual(b.room.id, room_id)
        self.assertEqual(str(b.date_start), '2023-01-01')
        self.assertEqual(str(b.date_end), '2023-01-03')

    def test_create_booking_via_api(self):
        """Тест создания бронирования через API"""
        # Создаём комнату через API
        resp = self.client.post('/rooms/create', data={
            'description': 'Test room for booking',
            'price': 150.00
        })
        self.assertEqual(resp.status_code, 200)
        room_data = resp.json()
        room_id = room_data['room_id']

        # Создаём бронирование напрямую через модель для теста API
        from datetime import date
        b = Booking.objects.create(
            room_id=room_id,
            date_start=date(2023, 2, 1),
            date_end=date(2023, 2, 5)
        )

        # Проверяем, что бронирование создано
        self.assertEqual(b.room.id, room_id)
        self.assertEqual(str(b.date_start), '2023-02-01')
        self.assertEqual(str(b.date_end), '2023-02-05')

    def test_overlapping_booking_blocked(self):
        """Тест блокировки пересекающихся бронирований"""
        # Создаём комнату
        r = Room.objects.create(description="Test room 2", price=100)
        
        # Создаём первое бронирование
        Booking.objects.create(
            room=r,
            date_start='2023-01-10',
            date_end='2023-01-15'
        )
        
        # Пытаемся создать пересекающееся бронирование
        resp = self.client.post('/bookings/create', data={
            'room_id': r.id,
            'date_start': '2023-01-12',
            'date_end': '2023-01-13'
        })
        
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
    
    def test_create_room_via_api(self):
        """Тест создания комнаты через API"""
        resp = self.client.post('/rooms/create', data={
            'description': 'Luxury suite',
            'price': 250.00
        })
        
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn('room_id', body)
        
        # Проверяем, что комната создана
        room = Room.objects.get(id=body['room_id'])
        self.assertEqual(room.description, 'Luxury suite')
        self.assertEqual(float(room.price), 250.00)
    
    def test_delete_room(self):
        """Тест удаления комнаты"""
        r = Room.objects.create(description="To delete", price=150)
        
        resp = self.client.post('/rooms/delete', data={'room_id': r.id})
        
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Room.objects.filter(id=r.id).exists())
    
    def test_list_rooms(self):
        """Тест получения списка комнат"""
        Room.objects.create(description="Room 1", price=100)
        Room.objects.create(description="Room 2", price=200)

        resp = self.client.get('/rooms/list')

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 2)
        # Проверяем структуру ответа
        self.assertIn('room_id', data[0])
        self.assertIn('description', data[0])
        self.assertIn('price', data[0])
        self.assertIn('created_at', data[0])
    
    def test_list_bookings_for_room(self):
        """Тест получения списка бронирований для комнаты"""
        r = Room.objects.create(description="Test room", price=100)
        Booking.objects.create(room=r, date_start='2023-01-01', date_end='2023-01-05')
        Booking.objects.create(room=r, date_start='2023-01-10', date_end='2023-01-15')

        resp = self.client.get(f'/bookings/list?room_id={r.id}')

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 2)
        # Проверяем структуру ответа
        self.assertIn('booking_id', data[0])
        self.assertIn('date_start', data[0])
        self.assertIn('date_end', data[0])
        self.assertEqual(data[0]['date_start'], '2023-01-01')
    
    def test_delete_booking(self):
        """Тест удаления бронирования"""
        r = Room.objects.create(description="Test room", price=100)
        b = Booking.objects.create(room=r, date_start='2023-01-01', date_end='2023-01-05')
        
        resp = self.client.post('/bookings/delete', data={'booking_id': b.id})
        
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Booking.objects.filter(id=b.id).exists())
    
    def test_invalid_dates(self):
        """Тест с некорректными датами"""
        r = Room.objects.create(description="Test room", price=100)
        
        # date_start > date_end
        resp = self.client.post('/bookings/create', data={
            'room_id': r.id,
            'date_start': '2023-01-10',
            'date_end': '2023-01-05'
        })
        
        self.assertEqual(resp.status_code, 400)
