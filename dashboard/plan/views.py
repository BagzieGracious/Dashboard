from .models import Plan
from .serializers import PlanSerializer
from ..authentication.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PlanApiView(generics.GenericAPIView):
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        plans = Plan.objects.all()
        if len(plans) < 1:
            return Response({'message': 'There are no plans.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanDetailsApiView(generics.GenericAPIView):
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        plans = Plan.objects.filter(id=id).first()
        context = { "request": request }
        if not plans:
            return Response({'errors': 'that plan was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = self.serializer_class(plans, context=context)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
