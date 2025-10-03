from django.core.exceptions import ValidationError
from django.db import models


class Room(models.Model):
    """Модель комнаты отеля"""
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена за ночь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ['id']

    def __str__(self):
        return f"Room {self.id} - {self.description[:30]}"


class Booking(models.Model):
    """Модель бронирования"""
    room = models.ForeignKey(
        Room, 
        related_name='bookings', 
        on_delete=models.CASCADE,
        verbose_name="Комната"
    )
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['room', 'date_start', 'date_end']),
        ]

    def __str__(self):
        return f"Booking {self.id} for Room {self.room_id}: {self.date_start} to {self.date_end}"

    def clean(self):
        """Валидация на уровне модели"""
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError("Дата начала не может быть позже даты окончания")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
