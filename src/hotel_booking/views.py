from django.http import JsonResponse


def rooms_create(request):
    return JsonResponse({"message": "room created (stub)"})


def rooms_delete(request):
    return JsonResponse({"message": "room deleted (stub)"})


def rooms_list(request):
    return JsonResponse([{"room_id": 1, "price": 100, "description": "Test room"}], safe=False)


def bookings_create(request):
    return JsonResponse({"message": "booking created (stub)"})


def bookings_delete(request):
    return JsonResponse({"message": "booking deleted (stub)"})


def bookings_list(request):
    data = [{"booking_id": 1, "date_start": "2025-10-03", "date_end": "2025-10-05"}]
    return JsonResponse(data, safe=False)
