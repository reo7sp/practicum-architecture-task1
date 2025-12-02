from rest_framework import serializers
from .models import Device


class DeviceRegistrationSerializer(serializers.Serializer):
    manufacturer_id = serializers.CharField(max_length=100)
    device_id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=255)
