from .models import App
from .serializers import AppSerializer
from ..authentication.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class AppDetailsApiView(generics.GenericAPIView):
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        apps = App.objects.filter(id=id).first()
        context = { "request": request }
        if not apps:
            return Response({'errors': 'that app was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = self.serializer_class(apps, context=context)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        data = request.data
        app = App.objects.filter(id=id).first()
        context = { "request": request }

        if app:
            serializer_data = self.serializer_class(app, data, partial=True, context=context)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response({ 'errors': 'that app was not found' }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        user = request.user
        app = App.objects.filter(user=user, id=id)

        if app:
            app.delete()
            return Response({'message': 'App has been deleted'}, status=status.HTTP_200_OK)
        return Response({'error': 'App does not exist in your list'}, status=status.HTTP_400_BAD_REQUEST)



class AppApiView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppSerializer

    def post(self, request):
        app = request.data
        serializer = self.serializer_class(data=app)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=User.objects.filter(email=request.user).first())

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        apps = App.objects.all()
        if len(apps) < 1:
            return Response({'message': 'There are no apps.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
