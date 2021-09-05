from django.core.exceptions import ValidationError
from django.db import models


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    gas_capacity = models.FloatField(default=100)
    gas_count = models.FloatField(default=100)

    @property
    def gas_count_percentage(self):
        if self.gas_capacity == 0:
            return 0
        return (self.gas_count * 100) / self.gas_capacity

    @property
    def status(self):
        return {
            "id": self.id,
            "gas_count_percentage": f"{self.gas_count_percentage}%",
            "gas_count_liters": self.gas_count,
            "tyres": [tyre.status for tyre in self.tyres.all()],
            "trips": [trip.status for trip in self.trips.all()],
            "maintenances": [mt.status for mt in self.maintenances.all()],
        }

    @classmethod
    def createCar(cls):
        """
        Creates a new instance of a car.

        :return: the instance of the car created.
        """

        car = cls.objects.create()

        for x in range(4):
            Tyre.createTyre(car=car)

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
                self.save()

                return self.gas_count_percentage

            return ValidationError(
                message="The ccurrent gas count must be less than 5% before refueling"
            )
        return ValidationError(
            message="Number of gas quantity to refuel surpasses the limit supported by the car"
        )

    def maintenance(self, tyre):
        """
        Swap a tyre that is degraded for a new one.

        :param Tyre tyre: a tyre which needs to be replaced.
        :return: the car instance.
        :raises: ValidationError: if the tyre's degradation is not higher than 94%.
        """

        if tyre.degradation > 94:
            tyre.delete()
            Tyre.createTyre(car=self)
            Maintenance.objects.create(car=self)

            return self
        return ValidationError(message="the tyre's degradation must be higher than 94%")

    def trip(self, distance=None):
        """
        Performs a trip.

        :param int distance: the distance of the trip in Km.
        :return: the car instance.
        """

        trip = None

        # Checks whether this is a new trip or a continuation of the last one
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
            if (trip.distance_travelled / 8).is_integer():
                self.gas_count -= 1

            if (trip.distance_travelled / 3).is_integer():
                for tyre in self.tyres.all():
                    tyre.degrade()
                    if tyre.degradation > 94:
                        has_degraded_tyres = True

            # Stop the trip
            if has_degraded_tyres:
                break
            if self.gas_count == 0:
                break

            # raise warnings
            for tyre in self.tyres.all():
                if tyre.degradation > 75:
                    raise ValidationError(
                        "Some tyres are with 75% of degradation, it's recomended to swap them as soon as possible",
                        code=400,
                    )
            if self.gas_count_percentage < 5:
                raise ValidationError(
                    "The current gas is less than 5%, it's recomended to refuel the car as soon as possible",
                    code=401,
                )

            trip.distance_travelled += 1
            trip.save()
            self.save()

        trip.finished = True
        trip.save()

        return self.status


class Tyre(models.Model):
    id = models.AutoField(primary_key=True)
    degradation = models.FloatField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="tyres")

    @property
    def degradation_percentage(self):
        return self.degradation

    @property
    def status(self):
        return {
            "id": self.id,
            "degradation": f"{self.degradation}%",
        }

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

    def degrade(self):
        """
        degrades the current tyre by 1%.

        :return: None
        :raises: ValidationError: if the tyre degradation is already at 100%.
        """
        if self.degradation < 100:
            self.degradation += 1
            self.save()
        return ValidationError(
            message="The tyre has already reached its maximum degradation of 100%"
        )


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    distance = models.FloatField()
    distance_travelled = models.FloatField(default=0)
    finished = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="trips")

    @property
    def status(self):
        return {
            "id": self.id,
            "distance": self.distance,
            "distance_travelled": self.distance_travelled,
            "finished": self.finished,
        }


class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="maintenances")
    date = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        return {"id": self.id, "date": self.date}
