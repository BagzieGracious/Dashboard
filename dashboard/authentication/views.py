import jwt
from .models import User
from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, exceptions
from django.contrib.sites.shortcuts import get_current_site
from .serializers import RegistrationSerializer, LoginSerializer, ResetPasswordSerializer, ChangePasswordSerializer


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serialiser = self.serializer_class(data=user)
        serialiser.is_valid(raise_exception=True)
        
        return Response(serialiser.data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        domain = request.META.get('HTTP_ORIGIN', get_current_site(request).domain)

        try:
            get_object_or_404(User, email=request.data['email'])
            token = str(jwt.encode({"email": request.data['email']}, settings.SECRET_KEY))
            link = f"{domain}/rest-auth/password/change/{token}"
            return Response(
                {
                    "message": "Kindly follow this link to reset your password",
                    "link": link
                },
                status=status.HTTP_200_OK)
        except KeyError:
            raise exceptions.ValidationError(
                "Email is required to reset a password")


class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def patch(self, request, token):
        try:
            payload = jwt.decode(token.strip(), settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.filter(email=payload.get('email')).first()
            if len(request.data['password']) >= 8:
                user.set_password(request.data['password'])
                user.save()

                return Response({
                    "message": "You have reset your password successfully."},
                    status=status.HTTP_200_OK)
            return Response({
                "error": "password should be atleast 8 characters."},
                status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({
                "error": "verification link is invalid."},
                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            raise exceptions.ValidationError("Password field is required.")
        except jwt.ExpiredSignatureError:
            return Response({
                "error": "verification link is expired"},
                status=status.HTTP_400_BAD_REQUEST)
