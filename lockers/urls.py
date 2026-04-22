from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LockerViewSet, ReservationViewSet, RegisterView

router = DefaultRouter()
router.register(r'lockers', LockerViewSet, basename='locker')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]