from rest_framework import serializers
from .models import HotelRoom, Booking
from datetime import datetime

class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['id', 'description', 'price_per_night', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room_id', 'date_start', 'date_end', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        if data['date_start'] > data['date_end']:
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
        
        # Проверка валидности дат (опционально)
        try:
            datetime.strptime(str(data['date_start']), '%Y-%m-%d')
            datetime.strptime(str(data['date_end']), '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError("Неверный формат даты. Используйте YYYY-MM-DD")
            
        return data
        
class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id')
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'date_start', 'date_end']

