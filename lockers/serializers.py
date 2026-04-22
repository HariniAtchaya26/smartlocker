from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Locker, Reservation

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # ✅ ensures password is hashed
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )

class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
