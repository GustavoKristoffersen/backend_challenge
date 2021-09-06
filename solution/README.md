## How to set up the project

Clone this repository and then execute the following commands

```
    cd backend_challenge

    cd solution

    pip install -r requirements.txt

    python manage.py migrate

```

To run the project execute

```
    python manage.py runserver
```

To run the test execute

```
    python manage.py test car_maintenance.tests
```

### API

| Endpoint      | Method | Query Params| Description|
| ----------- | ---------  |---------  |---------- |
| /cars/      | POST     |            | Creates a new car     | 
| /cars   | GET        || Returns a list of all the cars|
| /cars/{id}   | GET        || Returns details of the car|
| /cars/{id}/trip/   | POST  | distance < required if it's a new trip > | Starts a new trip or continue an unfinished trip. Returns the car status on trip end|
| /cars/{id}/maintain/   | POST        | tyre-id | Replaces a tyre of a car. Returns the car status|
| /cars/{id}/refuel/   | POST       | amount | Refuel the selected car. Returns the final gas count in %|
| /cars/{id}/create-tyre/ | POST     |    | Creates a new tyre for the selected car  |
