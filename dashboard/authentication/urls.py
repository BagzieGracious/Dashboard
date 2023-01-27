from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ResetPasswordAPIView, ChangePasswordAPIView


urlpatterns = [
    path('rest-auth/registration/', RegisterAPIView.as_view(), name='registration'),
    path('rest-auth/login/', LoginAPIView.as_view(), name='login'),
    path('rest-auth/password/reset/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('rest-auth/password/change/<token>', ChangePasswordAPIView.as_view(), name='password-change'),
]
