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

class RefuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refueling
        exclude = ['car']

class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        fields = ['id', 'degradation_percentage']


class CarSerializer(serializers.ModelSerializer):
    tyres = TyreSerializer(many=True)
    trips = TripSerializer(many=True)
    maintenances = serializers.SerializerMethodField()
    refuelings = serializers.SerializerMethodField()

    def get_maintenances(obj, self):
        return self.maintenances.count()

    def get_refuelings(obj, self):
        return self.refuelings.count()

    class Meta:
        model = Car
        fields = ['id', 'gas_capacity', 'gas_count', 'gas_count_percentage', 'tyres', 'maintenances', 'refuelings', 'trips']


#Use this serializer to get full details about maintenances and refuelings

# class CarSerializer(serializers.ModelSerializer):
#     tyres = TyreSerializer(many=True)
#     trips = TripSerializer(many=True)
#     maintenances = MaintenanceSerializer(many=True)
#     refuelings = RefuelingSerializer(many=True)

#     class Meta:
#         model = Car
#         fields = ['id', 'gas_capacity', 'gas_count', 'gas_count_percentage', 'tyres', 'trips', 'maintenances', 'refuelings']
#         read_only_fields = ['tyres', 'trips', 'maintenances', 'refuelings']


