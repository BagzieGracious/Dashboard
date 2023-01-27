from django.urls import path
from .views import SubscriptionApiView, SubscriptionDetailsApiView


urlpatterns = [
    path('subscriptions/', SubscriptionApiView.as_view(), name='list-subscription'),
    path('subscriptions/<id>', SubscriptionDetailsApiView.as_view(), name='get-subscription'),
]
