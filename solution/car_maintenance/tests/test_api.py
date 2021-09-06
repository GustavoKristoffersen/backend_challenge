from django.test import TestCase, Client
from django.urls import reverse
from car_maintenance.models import Car, Tyre

class TestCarViewSet(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cars_trip_POST_starts_trip(self):
        car = Car.objects.create()
        for i in range(4):
            Tyre.createTyre(car=car)

        url = reverse('cars-trip', args=[car.id])
        car = Car.objects.get(id=1)

        distance = 10000
        
        response = self.client.post(url, **{'QUERY_STRING': f'distance={distance}'})
        response_body = response.json()

        while response.status_code != 201:
            car = Car.objects.get(id=1)

            if 'degradation' in response_body.get('warning').get('message'):
                for tyre in car.tyres.all():
                    if tyre.is_degraded:
                        car.maintain(tyre)
                        print(f'Maintained {car.maintenances.count()} times')

            if 'gas' in response_body.get('warning').get('message'):
                car.refuel(50)
                print(f'Refueled {car.refuelings.count()} times')

            response = self.client.post(url)
            response_body = response.json()
        
        print(response_body)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response_body.get('trips')[0].get('distanceTravelled'), 10000)
        self.assertEquals(response_body.get('trips')[0].get('finished'), True)

        