from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Device
from .serializers import DeviceRegistrationSerializer


class RegisterDeviceView(APIView):
    def post(self, request):
        serializer = DeviceRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        manufacturer_id = serializer.validated_data['manufacturer_id']
        device_id = serializer.validated_data['device_id']
        name = serializer.validated_data['name']

        device, created = Device.objects.get_or_create(
            manufacturer_id=manufacturer_id,
            device_id=device_id,
            defaults={'name': name}
        )
        if not created:
            return Response({'error': 'Device already exists'}, status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_200_OK)


class UnregisterDeviceView(APIView):
    def delete(self, request, manufacturer_id, device_id):
        device = get_object_or_404(Device, manufacturer_id=manufacturer_id, device_id=device_id)
        device.delete()

        return Response(status=status.HTTP_200_OK)
