from rest_framework import serializers
from .models import User, Case
from subjects.serializers import MissingPersonSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'active']
        read_only_fields = ['id']


class CaseSerializer(serializers.ModelSerializer):
    missing_person = MissingPersonSerializer(read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'status', 'priority', 'assigned_to', 'assigned_to_detail', 'created_at', 'updated_at', 'missing_person']
