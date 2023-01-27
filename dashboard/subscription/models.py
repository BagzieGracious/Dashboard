from django.db import models
from ..app.models import App
from ..plan.models import Plan
from ..authentication.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscription')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_subscription')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='app_subscription')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
