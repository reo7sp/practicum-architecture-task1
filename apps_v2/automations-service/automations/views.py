from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Scenario
from .serializers import (
    ScenarioCreateSerializer,
    ScenarioSerializer,
    ScenarioCreateResponseSerializer
)


class CreateScenarioView(APIView):
    def post(self, request):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ScenarioCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        scenario = Scenario.objects.create(
            user_id=user_id,
            name=serializer.validated_data['name'],
            scenario=serializer.validated_data['scenario']
        )

        return Response(
            ScenarioCreateResponseSerializer({'id': scenario.id}).data,
            status=status.HTTP_200_OK
        )


class ListScenariosView(APIView):
    def get(self, request):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        scenarios = Scenario.objects.filter(user_id=user_id).order_by('-created_at')

        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data)


class ScenarioDetailView(APIView):
    def post(self, request, id):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        scenario = get_object_or_404(Scenario, id=id, user_id=user_id)

        serializer = ScenarioCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        scenario.name = serializer.validated_data['name']
        scenario.scenario = serializer.validated_data['scenario']
        scenario.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return Response({'error': 'X-User-ID header is required'}, status=status.HTTP_400_BAD_REQUEST)

        scenario = get_object_or_404(Scenario, id=id, user_id=user_id)
        scenario.delete()

        return Response(status=status.HTTP_200_OK)
