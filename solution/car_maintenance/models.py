from django.core.exceptions import ValidationError
from django.db import models

#Constant variables

#Average car capacity
DEFAULT_GAS_CAPACITY = 55
#If 3Km degrades 1% then 1Km degrades...
DEFAULT_DEGRADATION_PER_KM = 0.33
#If 8Km consumes 1 liter then 1Km consumes...
DEFAULT_GAS_CONSUMPTION_PER_KM = 0.125
#To be able to refuel the car gas must be less than...
DEFAULT_CONDITION_TO_REFUEL = 5
#To be able to swap a tyre, its degradation mus be higher than...
DEFAULT_CONDITION_TO_SWAP_TYRE = 94
#The system will raise a warning if the car's gas is less than...
DEFAULT_GAS_WARNING = 5
#The system will raise a warning if a tyre is with its degradation higher than...
DEFAULT_TYRE_DEGRADATION_WARNING = 94



class Car(models.Model):
    id = models.AutoField(primary_key=True)
    gas_capacity = models.FloatField(default=DEFAULT_GAS_CAPACITY)
    gas_count = models.FloatField(default=DEFAULT_GAS_CAPACITY)

    @property
    def gas_count_percentage(self):
        if self.gas_capacity == 0:
            return 0
        return (self.gas_count * 100) / self.gas_capacity

    @property
    def can_trip(self):
        if self.tyres.count() == 4 and self.gas_count > 0:
            return True
        return False

    def refuel(self, gas_quantity):
        f"""
        Refuel the car gas.

        :param float: the quantity of gas to be refueled in liters.
        :return: car instance
        :raises: ValidationError: if the gas quantity passed surpasses the limit supported by the car.
        :raises: ValidationError: if the car current gas count is not less than {DEFAULT_CONDITION_TO_REFUEL}%.
        """

        if gas_quantity + self.gas_count <= self.gas_capacity:
            if self.gas_count_percentage < DEFAULT_CONDITION_TO_REFUEL:
                self.gas_count += gas_quantity
                self.save()
                Refueling.objects.create(car=self, gas_amount=gas_quantity)

                return self

            raise ValidationError(
                message="The ccurrent gas count must be less than 5% before refueling"
            )
        raise ValidationError(
            message="Number of gas quantity to refuel surpasses the limit supported by the car"
        )

    def maintain(self, tyre):
        f"""
        Swap a tyre that is degraded for a new one.

        :param Tyre tyre: a tyre which needs to be replaced.
        :return: the car instance.
        :raises: ValidationError: if the tyre's degradation is not higher than {DEFAULT_CONDITION_TO_SWAP_TYRE}%.
        """

        if tyre.is_degraded:
            tyre.delete()
            Tyre.createTyre(car=self)
            Maintenance.objects.create(car=self)

            return self
        return ValidationError(message=f"the tyre's degradation must be higher than {DEFAULT_CONDITION_TO_SWAP_TYRE}%")

    def trip(self, distance=None):
        """
        Performs a trip.

        :param int distance: the distance of the trip in Km.
        :return: the car instance.
        """

        #Checks if the car can travel
        if not self.can_trip:
            raise Exception('The car is not in condition to travel. Make sure it has 4 tyres and gas > 0')

        # Checks whether this is a new trip or a continuation of the last one
        trip = None
        is_new_trip = True
        for t in self.trips.all():
            if t.finished == False:
                is_new_trip = False
                trip = t
                break

        if is_new_trip:
            trip = Trip.objects.create(distance=distance, car=self)

        # Starts trip
        has_degraded_tyres = False
        while trip.distance_travelled < trip.distance:

            # Stop the trip
            if has_degraded_tyres:
                break
            if self.gas_count == 0:
                break

            # raise warnings
            for tyre in self.tyres.all():
                if tyre.degradation > DEFAULT_TYRE_DEGRADATION_WARNING:
                    raise ValidationError(
                        f"Some tyres are with more than {DEFAULT_TYRE_DEGRADATION_WARNING}% of degradation, it's recomended to swap them as soon as possible"
                    )
            if self.gas_count_percentage < DEFAULT_GAS_WARNING:
                raise ValidationError(
                    f"The current gas is less than {DEFAULT_GAS_WARNING}%, it's recomended to refuel the car as soon as possible"
                )
            
            self.gas_count -= DEFAULT_GAS_CONSUMPTION_PER_KM

            for tyre in self.tyres.all():
                tyre.degrade(DEFAULT_DEGRADATION_PER_KM)
                if tyre.degradation >= 100:
                    has_degraded_tyres = True

            trip.distance_travelled += 1
            trip.save()
            self.save()

        trip.finished = True
        trip.save()

        return self


class Tyre(models.Model):
    id = models.AutoField(primary_key=True)
    degradation = models.FloatField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="tyres")

    @property
    def degradation_percentage(self):
        return self.degradation
    
    @property
    def is_degraded(self):
        return True if self.degradation > DEFAULT_CONDITION_TO_SWAP_TYRE else False

    @classmethod
    def createTyre(cls, car):
        """
        Creates a new tyre and adds it to an instance of car.

        :param Car car: a car instance to which the tyre is going to be added.
        :return: the instance of the tyre created.
        :raises: ValidationError: if the car already has 4 tyres.
        """

        if car.tyres.count() < 4:
            return cls.objects.create(car=car)
        raise ValidationError(
            message="Car instance exceeded the maximum limit of tyres"
        )

    def degrade(self, quantity):
        """
        degrades the current tyre by the passed value.

        :return: instance of tyre
        :raises: ValidationError: if the tyre degradation is already at 100%.
        """
        if self.degradation < 100:
            self.degradation += quantity
            self.save()
            return self
            
        return ValidationError(
            message="The tyre has already reached its maximum degradation of 100%"
        )


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    distance = models.FloatField()
    distance_travelled = models.FloatField(default=0)
    finished = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="trips")


class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="maintenances")
    date = models.DateTimeField(auto_now_add=True)

class Refueling(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='refuelings')
    gas_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
