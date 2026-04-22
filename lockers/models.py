from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('user', 'User'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
class Locker(models.Model):
    locker_number = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='available')  # available/occupied/deactivated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
