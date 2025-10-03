from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import (
    BookingListSerializer,
    BookingSerializer,
    RoomCreateSerializer,
    RoomSerializer,
)


class RoomCreateView(APIView):
    """Создание комнаты"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            return Response({'room_id': room.id}, status=status.HTTP_200_OK)
        return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class RoomDeleteView(APIView):
    """Удаление комнаты"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        room_id = request.data.get('room_id')
        if not room_id:
            return Response({'error': 'room_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response({'ok': True}, status=status.HTTP_200_OK)


class RoomListView(APIView):
    """Список комнат с сортировкой"""
    permission_classes = [AllowAny]

    def get(self, request):
        sort_by = request.query_params.get('sort_by', 'id')
        order = request.query_params.get('order', 'asc')

        # Маппинг полей для сортировки
        sort_field_map = {
            'price': 'price',
            'created': 'created_at',
            'created_at': 'created_at',
            'id': 'id'
        }

        field = sort_field_map.get(sort_by, 'id')

        if order == 'desc':
            field = f'-{field}'

        rooms = Room.objects.all().order_by(field)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingCreateView(APIView):
    """Создание бронирования"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Получаем данные
        room_id = request.data.get('room_id')
        date_start = request.data.get('date_start')
        date_end = request.data.get('date_end')
        
        # Базовая валидация
        if not room_id or not date_start or not date_end:
            return Response(
                {'error': 'room_id, date_start and date_end are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка существования комнаты
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {'error': 'room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Подготовка данных для сериализатора
        data = {
            'room': room.id,
            'date_start': date_start,
            'date_end': date_end
        }
        
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            try:
                booking = serializer.save()
                return Response({'booking_id': booking.id}, status=status.HTTP_200_OK)
            except Exception:
                return Response(
                    {'error': 'room is already booked on given dates'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Обработка ошибок валидации
        errors = serializer.errors
        if any('уже забронирована' in str(error) for error in errors.values()):
            return Response(
                {'error': 'room is already booked on given dates'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'error': str(errors)}, status=status.HTTP_400_BAD_REQUEST)


class BookingDeleteView(APIView):
    """Удаление бронирования"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response(
                {'error': 'booking_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return Response({'ok': True}, status=status.HTTP_200_OK)


class BookingListView(APIView):
    """Список бронирований для комнаты"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response(
                {'error': 'room_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {'error': 'room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        bookings = Booking.objects.filter(room=room).order_by('date_start')
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
