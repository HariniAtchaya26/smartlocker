from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Locker, Reservation
from .serializers import UserSerializer, LockerSerializer, ReservationSerializer
import redis   # direct Redis client

User = get_user_model()

# Redis connection
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LockerViewSet(viewsets.ModelViewSet):
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        # Query DB for available lockers
        lockers = Locker.objects.filter(status='available')
        serializer = self.get_serializer(lockers, many=True)
        data = serializer.data

        # Direct write to Redis
        r.set('available_lockers', str(data))

        return Response(data)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=True, methods=['put'])
    def release(self, request, pk=None):
        reservation = self.get_object()
        reservation.released_at = timezone.now()
        reservation.save()
        reservation.locker.status = 'available'
        reservation.locker.save()
        return Response({"message": "Locker released"})
