from django.core.exceptions import ValidationError
from django.db import models

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    gas_capacity = models.FloatField(default=100)
    gas_count = models.FloatField(default=0)
    
class Tyre(models.Model):
    id = models.AutoField(primary_key=True)
    degradation = models.FloatField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='tyres')
    
    @classmethod
    def createTyre(cls, car):
        """
        Creates a new tyre and adds it to an instance of car.

        :param car: a car instance to which the tyre is going to be added.
        :return: the instance of the tyre created.
        :raises: ValidationError: if the car already has 4 tyres.
        """

        if car.tyres.count() < 4:
            return cls.objects.create(car=car)
        raise ValidationError(message='Car instance exceeded the maximum limit of tyres')