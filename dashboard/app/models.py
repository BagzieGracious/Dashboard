from django.db import models
from ..authentication.models import User
from django.utils.translation import gettext_lazy as _


class App(models.Model):
    class TypeChoices(models.TextChoices):
        WEB = 'Web', _('Web')
        MOBILE = 'Mobile', _('Mobile')
    
    class FrameworkChoices(models.TextChoices):
        DJANGO = 'Django', _('Django')
        REACT = 'React', _('React')

    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(
        max_length=6, choices=TypeChoices.choices, 
        default=TypeChoices.WEB)
    framework = models.CharField(
        max_length=6, choices=FrameworkChoices.choices, 
        default=FrameworkChoices.DJANGO)

    domain_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_app')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
