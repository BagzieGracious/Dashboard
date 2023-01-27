from django.urls import path
from .views import (AppDetailsApiView, AppApiView)


urlpatterns = [
    path('apps/', AppApiView.as_view(), name='list-apps'),
    path('apps/<id>', AppDetailsApiView.as_view(), name='get-apps'),
]
