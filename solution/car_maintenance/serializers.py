from rest_framework import serializers
from car_maintenance.models import *

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        exclude = ['car']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        exclude = ['car']

class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        exclude = ['car']

class CarSerializer(serializers.ModelSerializer):
    tyres = TyreSerializer(many=True)
    trips = TripSerializer(many=True)
    maintenances = MaintenanceSerializer(many=True)

    class Meta:
        model = Car
        fields = ['id', 'gas_capacity', 'gas_count', 'gas_count_percentage', 'tyres', 'trips', 'maintenances']