from django.urls import path
from .views import PlanApiView, PlanDetailsApiView


urlpatterns = [
    path('plans/', PlanApiView.as_view(), name='list-plans'),
    path('plans/<id>', PlanDetailsApiView.as_view(), name='get-plan'),
]
