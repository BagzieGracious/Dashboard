from ..app.models import App
from ..plan.models import Plan
from .models import Subscription
from ..authentication.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated


class SubscriptionApiView(generics.GenericAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        subscription = request.data
        serializer = self.serializer_class(data=subscription)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=request.user).first()
        plan = Plan.objects.filter(id=request.data['plan']).first()
        if not plan:
            return Response({'errors': 'that plan was not found'}, status=status.HTTP_404_NOT_FOUND)

        app = App.objects.filter(id=request.data['app']).first()
        if not app:
            return Response({'errors': 'that app was not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(user=user, plan=plan, app=app)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user)
        if len(subscription) < 1:
            return Response({'message': 'There are no subscription.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(subscription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SubscriptionDetailsApiView(generics.GenericAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        subscription = Subscription.objects.filter(id=id).first()
        context = { "request": request }
        if not subscription:
            return Response({'errors': 'that subscription was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = self.serializer_class(subscription, context=context)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        data = request.data
        subscription = Subscription.objects.filter(id=id).first()
        context = { "request": request }

        if subscription:
            serializer_data = self.serializer_class(subscription, data, partial=True, context=context)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response({ 'errors': 'that subscription was not found' }, status=status.HTTP_404_NOT_FOUND)
