from django.urls import path

from .views import (
    BookingCreateView,
    BookingDeleteView,
    BookingListView,
    RoomCreateView,
    RoomDeleteView,
    RoomListView,
)

app_name = 'api'

urlpatterns = [
    # Room endpoints
    
    path('rooms/create', RoomCreateView.as_view(), name='room_create'),
    path('rooms/delete', RoomDeleteView.as_view(), name='room_delete'),
    path('rooms/list', RoomListView.as_view(), name='room_list'),
    
    # Booking endpoints
    path('bookings/create', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/delete', BookingDeleteView.as_view(), name='booking_delete'),
    path('bookings/list', BookingListView.as_view(), name='booking_list'),
]
