from django.urls import path
from .views import (
    HotelRoomCreateView, HotelRoomDeleteView, HotelRoomListView,
    BookingCreateView, BookingDeleteView, BookingListView
)

urlpatterns = [
    path('hotel-rooms/create/', HotelRoomCreateView.as_view(), name='hotel_room_create'),
    path('hotel-rooms/delete/', HotelRoomDeleteView.as_view(), name='hotel_room_delete'),
    path('hotel-rooms/list/', HotelRoomListView.as_view(), name='hotel_room_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path('bookings/list/', BookingListView.as_view(), name='booking_list'),
]
