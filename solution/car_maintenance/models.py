from django.core.exceptions import ValidationError
from django.db import models

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    gas_capacity = models.FloatField(default=100)
    gas_count_liters = models.FloatField(default=100)
    
    @property
    def gas_count_percentage(self,):
        return f'{(self.gas_capacity * 100) / self.gas_count_liters}%'

    @classmethod
    def createCar(cls, gas_capacity):
        """
        Creates a new instance of a car.

        :param float: the gas capacity of the car in liter.
        :return: the instance of the car created.
        """

        car = cls.objects.create(gas_capacity=gas_capacity)
        for x in range(4):
            tyre = Tyre.objects.create(car=car)
        
        return car

    
    def refuel(self, gas_quantity):
        """
        Refuel the car gas.

        :param float: the quantity in liters of gas to be refuled.
        :return: the current gas count of the car in %.
        :raises: ValidationError: if the gas quantity passed surpasses the limit supported by the car.
        """

        if gas_quantity + self.gas_count_liters <= self.gas_capacity:
            self.gas_count_liters += gas_quantity
            return self.gas_count_percentage
        return ValidationError(message='Number of gas quantity to refuel surpasses the limit supported by the car')

    
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