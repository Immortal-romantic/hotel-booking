from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

"""
URL configuration for hotel_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for hotel_booking project.
"""


def api_overview(request):
    """Обзор доступных API эндпоинтов"""
    return JsonResponse({
        "name": "Hotel Booking API",
        "version": "1.0.0",
        "description": "API для управления номерами отелей и бронированиями",
        "endpoints": {
            "rooms": {
                "create": "POST /rooms/create",
                "delete": "POST /rooms/delete",
                "list": "GET /rooms/list"
            },
            "bookings": {
                "create": "POST /bookings/create",
                "delete": "POST /bookings/delete",
                "list": "GET /bookings/list"
            }
        },
        "documentation": "/README.md",
        "github": "https://github.com/your-repo/hotel-booking"
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_overview, name='api_overview'),  # Корневой путь с информацией об API
    path('api/', include('api.urls')),  # API эндпоинты под /api/
]
