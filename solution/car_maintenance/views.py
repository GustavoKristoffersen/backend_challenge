from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from car_maintenance.models import Car
from car_maintenance.serializers import CarSerializer

class CarViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    @action(methods=['POST'], detail=True)
    def trip(self, request, id, *args, **kwargs):
        distance = int(request.query_params.get('distance'))
        car = Car.objects.get(id=id)
        try:
            car.trip(distance) if distance else car.trip()
            serializer = CarSerializer(car)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                'warning': {
                    'code': e.code,
                    'msg': e.message
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    