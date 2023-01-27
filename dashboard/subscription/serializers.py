from .models import App
from .models import Subscription
from rest_framework import serializers
from ..app.serializers import AppSerializer
from ..plan.serializers import PlanSerializer



class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    active = serializers.BooleanField()
    plan = PlanSerializer(read_only=True)
    app = AppSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'app', 'active', 'created_at', 'updated_at']

