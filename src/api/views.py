from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import HotelRoom, Booking


class HotelRoomModelTest(TestCase):
    """Тесты для модели HotelRoom"""
    
    def test_create_hotel_room(self):
        """Тестирование создания номера отеля"""
        room = HotelRoom.objects.create(
            description="Люкс с видом на море",
            price_per_night=10000,
            capacity=2
        )
        
        self.assertEqual(room.description, "Люкс с видом на море")
        self.assertEqual(room.price_per_night, 10000)
        self.assertEqual(room.capacity, 2)
        self.assertIsNotNone(room.created_at)


class BookingModelTest(TestCase):
    """Тесты для модели Booking"""
    
    def setUp(self):
        """Создание тестового номера для бронирования"""
        self.room = HotelRoom.objects.create(
            description="Стандартный номер",
            price_per_night=5000,
            capacity=2
        )
    
    def test_create_booking(self):
        """Тестирование создания бронирования"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        booking = Booking.objects.create(
            room=self.room,
            guest_name="Иван Иванов",
            guest_email="ivan@example.com",
            date_start=today,
            date_end=tomorrow
        )
        
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.guest_name, "Иван Иванов")
        self.assertEqual(booking.guest_email, "ivan@example.com")
        self.assertEqual(booking.date_start, today)
        self.assertEqual(booking.date_end, tomorrow)


class HotelRoomAPITest(TestCase):
    """Тесты API для работы с номерами отелей"""
    
    def setUp(self):
        """Подготовка клиента API и тестовых данных"""
        self.client = APIClient()
        self.room_data = {
            "description": "Двухместный номер",
            "price_per_night": 6000,
            "capacity": 2
        }
        
        # Создаем тестовый номер
        self.room = HotelRoom.objects.create(
            description="Люкс",
            price_per_night=12000,
            capacity=4
        )
    
    def test_create_hotel_room(self):
        """Тест создания номера через API"""
        url = reverse('hotel_room_create')
        response = self.client.post(url, self.room_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('room_id', response.data)
        
        # Проверяем, что номер действительно создался
        room_id = response.data['room_id']
        room = HotelRoom.objects.get(id=room_id)
        self.assertEqual(room.description, self.room_data['description'])
        self.assertEqual(room.price_per_night, self.room_data['price_per_night'])
    
    def test_delete_hotel_room(self):
        """Тест удаления номера через API"""
        url = reverse('hotel_room_delete')
        data = {"room_id": self.room.id}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что номер удален
        self.assertFalse(HotelRoom.objects.filter(id=self.room.id).exists())
    
    def test_delete_nonexistent_room(self):
        """Тест удаления несуществующего номера"""
        url = reverse('hotel_room_delete')
        data = {"room_id": 9999}  # Несуществующий ID
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_hotel_rooms(self):
        """Тест получения списка номеров"""
        # Создаем еще один номер для проверки сортировки
        HotelRoom.objects.create(
            description="Бюджетный номер",
            price_per_night=3000,
            capacity=1
        )
        
        url = reverse('hotel_room_list')
        
        # Тест без параметров сортировки
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Тест с сортировкой по цене (по возрастанию)
        response = self.client.get(f"{url}?sort_by=price_per_night&order=asc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price_per_night'], 3000)
        self.assertEqual(response.data[1]['price_per_night'], 12000)
        
        # Тест с сортировкой по цене (по убыванию)
        response = self.client.get(f"{url}?sort_by=price_per_night&order=desc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price_per_night'], 12000)
        self.assertEqual(response.data[1]['price_per_night'], 3000)
        
        # Тест с некорректным параметром сортировки
        response = self.client.get(f"{url}?sort_by=invalid_field")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookingAPITest(TestCase):
    """Тесты API для работы с бронированиями"""
    
    def setUp(self):
        """Подготовка клиента API и тестовых данных"""
        self.client = APIClient()
        
        # Создаем тестовый номер
        self.room = HotelRoom.objects.create(
            description="Стандартный номер",
            price_per_night=5000,
            capacity=2
        )
        
        # Даты для тестирования
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after_tomorrow = self.today + timedelta(days=2)
        
        # Данные для создания бронирования
        self.booking_data = {
            "room_id": self.room.id,
            "guest_name": "Петр Петров",
            "guest_email": "petr@example.com",
            "date_start": self.tomorrow.isoformat(),
            "date_end": self.day_after_tomorrow.isoformat()
        }
    
    def test_create_booking(self):
        """Тест создания бронирования"""
        url = reverse('booking_create')
        response = self.client.post(url, self.booking_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('booking_id', response.data)
        
        # Проверяем, что бронирование создалось
        booking_id = response.data['booking_id']
        booking = Booking.objects.get(id=booking_id)
        self.assertEqual(booking.room.id, self.booking_data['room_id'])
        self.assertEqual(booking.guest_name, self.booking_data['guest_name'])
        self.assertEqual(booking.guest_email, self.booking_data['guest_email'])
    
    def test_create_booking_nonexistent_room(self):
        """Тест создания бронирования для несуществующего номера"""
        url = reverse('booking_create')
        data = self.booking_data.copy()
        data['room_id'] = 9999  # Несуществующий ID
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_create_overlapping_booking(self):
        """Тест создания перекрывающегося бронирования"""
        # Создаем первое бронирование
        url = reverse('booking_create')
        self.client.post(url, self.booking_data, format='json')
        
        # Пытаемся создать второе бронирование на те же даты
        response = self.client.post(url, self.booking_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('забронирован', response.data['error'])
    
    def test_delete_booking(self):
        """Тест удаления бронирования"""
        # Сначала создаем бронирование
        create_url = reverse('booking_create')
        create_response = self.client.post(create_url, self.booking_data, format='json')
        booking_id = create_response.data['booking_id']
        
        # Теперь удаляем его
        delete_url = reverse('booking_delete')
        delete_data = {"booking_id": booking_id}
        delete_response = self.client.post(delete_url, delete_data, format='json')
        
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что бронирование удалено
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())
    
    def test_delete_nonexistent_booking(self):
        """Тест удаления несуществующего бронирования"""
        url = reverse('booking_delete')
        data = {"booking_id": 9999}  # Несуществующий ID
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_bookings(self):
        """Тест получения списка бронирований по номеру"""
        # Создаем бронирование
        create_url = reverse('booking_create')
        self.client.post(create_url, self.booking_data, format='json')
        
        # Получаем список бронирований
        list_url = reverse('booking_list')
        response = self.client.get(f"{list_url}?room_id={self.room.id}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['guest_name'], self.booking_data['guest_name'])
    
    def test_list_bookings_no_room_id(self):
        """Тест получения списка бронирований без указания room_id"""
        list_url = reverse('booking_list')
        response = self.client.get(list_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_list_bookings_nonexistent_room(self):
        """Тест получения списка бронирований для несуществующего номера"""
        list_url = reverse('booking_list')
        response = self.client.get(f"{list_url}?room_id=9999")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
