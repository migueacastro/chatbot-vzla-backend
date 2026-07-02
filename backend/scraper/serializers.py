from rest_framework import serializers
from .models import Source, Investigation, SourceResult

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class SourceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceResult
        fields = '__all__'


class InvestigationSerializer(serializers.ModelSerializer):
    results = SourceResultSerializer(many=True, read_only=True)

    class Meta:
        model = Investigation
        fields = ['id', 'case', 'assigned_to', 'status', 'started_at', 'finished_at', 'results']
