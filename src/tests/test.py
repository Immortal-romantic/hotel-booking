# tests.py
import pytest
import datetime
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from hotel_booking import HotelRoom, Booking

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def hotel_room():
    room = HotelRoom.objects.create(
        description="Тестовый номер",
        price_per_night=1000,
        capacity=2
    )
    return room

@pytest.mark.django_db
class TestHotelRoomAPI:
    def test_create_hotel_room(self, api_client):
        url = reverse('hotel_room_create')
        data = {
            "description": "Люкс с видом на море",
            "price_per_night": 5000,
            "capacity": 2
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'room_id' in response.data
        assert HotelRoom.objects.count() == 1
        
    def test_delete_hotel_room(self, api_client, hotel_room):
        url = reverse('hotel_room_delete')
        data = {"room_id": hotel_room.id}
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert HotelRoom.objects.count() == 0
        
    def test_list_hotel_rooms(self, api_client, hotel_room):
        # Создадим еще один номер для сортировки
        HotelRoom.objects.create(
            description="Второй тестовый номер",
            price_per_night=2000,
            capacity=3
        )
        
        # Тест без параметров сортировки
        url = reverse('hotel_room_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        
        # Тест с сортировкой по цене (возрастание)
        url = f"{reverse('hotel_room_list')}?sort_by=price_per_night&order=asc"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['price_per_night'] < response.data[1]['price_per_night']
        
        # Тест с сортировкой по цене (убывание)
        url = f"{reverse('hotel_room_list')}?sort_by=price_per_night&order=desc"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['price_per_night'] > response.data[1]['price_per_night']

@pytest.mark.django_db
class TestBookingAPI:
    def test_create_booking(self, api_client, hotel_room):
        url = reverse('booking_create')
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        data = {
            "room_id": hotel_room.id,
            "guest_name": "Иван Петров",
            "guest_email": "ivan@example.com",
            "date_start": today.isoformat(),
            "date_end": tomorrow.isoformat()
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'booking_id' in response.data
        assert Booking.objects.count() == 1
    
    def test_create_booking_room_not_found(self, api_client):
        url = reverse('booking_create')
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        data = {
            "room_id": 999,  # несуществующий ID
            "guest_name": "Иван Петров",
            "guest_email": "ivan@example.com",
            "date_start": today.isoformat(),
            "date_end": tomorrow.isoformat()
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_overlapping_bookings(self, api_client, hotel_room):
        # Создаем первую бронь
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=5)
        
        Booking.objects.create(
            room=hotel_room,
            guest_name="Тестовый гость",
            guest_email="test@example.com",
            date_start=today,
            date_end=end_date
        )
        
 