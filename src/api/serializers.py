from rest_framework import serializers
from django.db.models import Q
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Room"""
    room_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Room
        fields = ['room_id', 'description', 'price', 'created_at']
        read_only_fields = ['room_id', 'created_at']

    def validate_price(self, value):
        """Валидация цены"""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


class RoomCreateSerializer(serializers.Serializer):
    """Сериализатор для создания комнаты (поддержка двух вариантов поля)"""
    description = serializers.CharField(required=False, allow_blank=False)
    text = serializers.CharField(required=False, allow_blank=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        # Поддержка обоих полей: description или text
        desc = data.get('description') or data.get('text')
        if not desc or desc.strip() == '':
            raise serializers.ValidationError({
                'description': 'Требуется поле description или text, и оно не должно быть пустым'
            })
        data['description'] = desc.strip()
        return data

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена должна быть неотрицательной")
        return value

    def create(self, validated_data):
        validated_data.pop('text', None)  # Удаляем text если был передан
        return Room.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Booking"""
    booking_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'room_id', 'date_start', 'date_end', 'created_at']
        read_only_fields = ['booking_id', 'created_at']

    def validate(self, data):
        """Валидация дат"""
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        if date_start and date_end and date_start > date_end:
            raise serializers.ValidationError({
                'date_end': 'Дата окончания должна быть не раньше даты начала'
            })
        
        return data

    def validate_room_overlap(self, room, date_start, date_end, exclude_id=None):
        """Проверка пересечения дат для комнаты"""
        overlapping_bookings = Booking.objects.filter(
            room=room
        ).filter(
            ~Q(date_end__lt=date_start) & ~Q(date_start__gt=date_end)
        )
        
        # Исключаем текущее бронирование при обновлении
        if exclude_id:
            overlapping_bookings = overlapping_bookings.exclude(id=exclude_id)
        
        if overlapping_bookings.exists():
            raise serializers.ValidationError({
                'room_id': 'Комната уже забронирована на указанные даты'
            })

    def create(self, validated_data):
        """Создание бронирования с проверкой пересечений"""
        room = validated_data['room']
        date_start = validated_data['date_start']
        date_end = validated_data['date_end']
        
        self.validate_room_overlap(room, date_start, date_end)
        return Booking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление бронирования с проверкой пересечений"""
        room = validated_data.get('room', instance.room)
        date_start = validated_data.get('date_start', instance.date_start)
        date_end = validated_data.get('date_end', instance.date_end)
        
        self.validate_room_overlap(room, date_start, date_end, exclude_id=instance.id)
        
        instance.room = room
        instance.date_start = date_start
        instance.date_end = date_end
        instance.save()
        return instance


class BookingListSerializer(serializers.ModelSerializer):
    """Упрощённый сериализатор для списка бронирований"""
    booking_id = serializers.IntegerField(source='id')
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'date_start', 'date_end']
