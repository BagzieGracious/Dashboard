from .models import App
from rest_framework import serializers
from ..authentication.serializers import UserSerializer


class AppSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    user = UserSerializer(read_only=True)
    description = serializers.CharField()
    type = serializers.CharField()
    framework = serializers.CharField(max_length=6)
    domain_name = serializers.CharField(max_length=50)
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = App
        fields = ['id', 'user', 'name', 'description', 'type', 'framework', 'domain_name', 'created_at', 'updated_at']
