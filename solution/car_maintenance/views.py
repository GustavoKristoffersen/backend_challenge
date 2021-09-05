from car_maintenance.models import Car
from car_maintenance.serializers import CarSerializer
from rest_framework.viewsets import ModelViewSet

class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()