from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaProducer
import json
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


class ExecuteActionView(APIView):
    def post(self, request, manufacturer_id, device_id, action_id):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        event = {
            'user_id': user_id,
            'manufacturer_id': manufacturer_id,
            'device_id': device_id,
            'action_id': action_id,
        }

        try:
            future = producer.send(settings.KAFKA_TOPIC, event)
            future.get(timeout=10)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
