from django.core.exceptions import ValidationError
from django.db import models

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    gas_capacity = models.FloatField(default=100)
    gas_count = models.FloatField(default=100)

    @property
    def gas_count_percentage(self,):
        if self.gas_capacity == 0:
            return 0
        return (self.gas_count * 100) / self.gas_capacity

    @classmethod
    def createCar(cls, gas_capacity=None):
        """
        Creates a new instance of a car.

        :param float: the gas capacity of the car in liter.
        :return: the instance of the car created.
        """

        if gas_capacity:
            car = cls.objects.create(gas_capacity=gas_capacity, gas_count=gas_capacity)
        else:
            car = cls.objects.create()
            
        for x in range(4):
            tyre = Tyre.createTyre(car=car)
        
        return car

    
    def refuel(self, gas_quantity):
        """
        Refuel the car gas.

        :param float: the quantity in liters of gas to be refuled.
        :return: the current gas count of the car in %.
        :raises: ValidationError: if the gas quantity passed surpasses the limit supported by the car.
        :raises: ValidationError: if the car current gas count is higher than 5%.
        """

        if gas_quantity + self.gas_count <= self.gas_capacity:
            if self.gas_count_percentage < 5:
                self.gas_count += gas_quantity
                return self.gas_count_percentage
            return ValidationError(message='The ccurrent gas count must be less than 5% before refueling')
        return ValidationError(message='Number of gas quantity to refuel surpasses the limit supported by the car')

    def maintenance(self, tyre):
        """
        Swap a tyre that is degradated for a new one.

        :param tyre: a tyre which needs to be replaced.
        :return: the car instance.
        :raises: ValidationError: if the tyre's degradation is not higher than 94%.
        """
        
        if tyre.degradation > 94:
            tyre.delete()
            Tyre.createTyre(car=self)

            return self
        return ValidationError(message="the tyre's degradation must be higher than 94%")        


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

    def degradate(self,):
        """
        Deagradates the current tyre by 1%.

        :return: None
        :raises: ValidationError: if the tyre degradation is already at 100%.
        """
        if self.degradation < 100:
            self.degradation += 1
        return ValidationError(message='The tyre has already reached its maximum degradation of 100%')