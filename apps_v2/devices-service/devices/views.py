from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Device
from .serializers import DeviceSerializer, DeviceRegistrationSerializer
import requests
from django.conf import settings


class DeviceListView(APIView):
    def get(self, request):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        devices = Device.objects.filter(user_id=user_id)

        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        manufacturer_id = serializer.validated_data['manufacturer_id']
        device_id = serializer.validated_data['device_id']
        name = serializer.validated_data['name']

        try:
            integration_response = requests.post(
                f'{settings.INTEGRATION_SERVICE_URL}/api/v1/devices/',
                json={
                    'manufacturer_id': manufacturer_id,
                    'device_id': device_id,
                    'name': name,
                },
                timeout=settings.INTEGRATION_SERVICE_TIMEOUT
            )
            if integration_response.status_code not in [200, 201]:
                return Response(
                    {'error': 'Failed to register device with integration service'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except requests.RequestException:
            return Response(
                {'error': 'Integration service unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        device, created = Device.objects.get_or_create(
            manufacturer_id=manufacturer_id,
            device_id=device_id,
            defaults={
                'user_id': user_id,
                'name': name,
            }
        )
        if not created:
            return Response({'error': 'Device already exists'}, status=status.HTTP_409_CONFLICT)

        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)


class DeviceDetailView(APIView):
    def delete(self, request, manufacturer_id, device_id):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        device = get_object_or_404(Device, manufacturer_id=manufacturer_id, device_id=device_id, user_id=user_id)

        try:
            integration_response = requests.delete(
                f'{settings.INTEGRATION_SERVICE_URL}/api/v1/devices/{manufacturer_id}/{device_id}',
                timeout=settings.INTEGRATION_SERVICE_TIMEOUT
            )
            if integration_response.status_code not in [200, 204]:
                return Response(
                    {'error': 'Failed to unregister device with integration service'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except requests.RequestException:
            return Response(
                {'error': 'Integration service unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        device.delete()

        return Response(status=status.HTTP_200_OK)
