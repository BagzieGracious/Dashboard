from .models import Plan
from rest_framework import serializers


class PlanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    price = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'price']
