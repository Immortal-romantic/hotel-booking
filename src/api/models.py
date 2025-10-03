from django.db import models

class HotelRoom(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hotel_rooms'
        indexes = [
            models.Index(fields=['price_per_night']),
            models.Index(fields=['created_at'])
        ]

class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='bookings')
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookings'
        indexes = [
            models.Index(fields=['date_start']),
            models.Index(fields=['room', 'date_start'])
        ]


