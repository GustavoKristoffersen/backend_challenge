from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from car_maintenance.models import Car, Tyre
from car_maintenance.serializers import CarSerializer, TyreSerializer

class CarViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def create(self, request, *args, **kwargs):
        car = Car.objects.create()
        serializer = CarSerializer(car)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def trip(self, request, id, *args, **kwargs):
        distance = request.query_params.get('distance')

        if distance:
            distance = int(distance)
        
        car = Car.objects.get(id=id)
        try:
            car.trip(distance) if distance else car.trip()
            serializer = CarSerializer(car)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'warning': {'message': e.message}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': {'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(methods=['POST'], detail=True)
    def refuel(self, request, id, *args, **kwargs):
        car = Car.objects.get(id=id)
        gas = int(request.query_params.get('gas'))

        try:
            car.refuel(gas)
        except ValidationError as e:
            return Response(data={'error': {'message': e.message}}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'car_id': car.id, 'gas_count_percentage': car.gas_count_percentage})
    
    @action(methods=['POST'], detail=True)
    def maintain(self, request, id, *args, **kwargs):
        car = Car.objects.get(id=id)
        tyre_id = int(request.query_params.get('tyre-id'))
        tyre = Tyre.objects.get(id=tyre_id)

        if tyre not in car.tyres.all():
            return Response(data={'error':{'message': 'The scpecified tyre is not a component of this car'}})

        try:
            car.maintain(tyre)
        except ValidationError as e:
            return Response(data={'error': {'message': e.message}}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CarSerializer(car)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST'], detail=True, url_path='create-tyre')
    def create_tyre(self, request, id, *args, **kwargs):
        car = Car.objects.get(id=id)
        try:
            tyre = Tyre.createTyre(car)
        except ValidationError as e:
            return Response(data={'error': {'message': e.message}}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TyreSerializer(tyre)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)