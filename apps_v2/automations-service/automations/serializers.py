from rest_framework import serializers
from .models import Scenario


class ScenarioCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    scenario = serializers.JSONField()


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'name', 'scenario']


class ScenarioCreateResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
