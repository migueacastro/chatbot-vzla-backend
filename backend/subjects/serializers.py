from rest_framework import serializers
from .models import MissingPerson, Alias, Relative, LocationHistory

class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = '__all__'


class RelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relative
        fields = '__all__'


class LocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationHistory
        fields = '__all__'


class MissingPersonSerializer(serializers.ModelSerializer):
    aliases = AliasSerializer(many=True, read_only=True)
    relatives = RelativeSerializer(many=True, read_only=True)
    location_history = LocationHistorySerializer(many=True, read_only=True)

    class Meta:
        model = MissingPerson
        fields = [
            'id', 'case', 'first_name', 'middle_name', 'last_name', 
            'second_last_name', 'full_name', 'birth_date', 'gender', 
            'nationality', 'document_number', 'status', 'notes', 
            'photo_url', 'aliases', 'relatives', 'location_history'
        ]
        read_only_fields = ['full_name']
