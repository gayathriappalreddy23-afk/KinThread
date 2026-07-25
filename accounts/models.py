from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, default="+91 9876543210", blank=True)
    address = models.TextField(default="KinThread Fashion House, MG Road, Suite 402", blank=True)
    city = models.CharField(max_length=100, default="Bengaluru, Karnataka", blank=True)
    pincode = models.CharField(max_length=10, default="560001", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
