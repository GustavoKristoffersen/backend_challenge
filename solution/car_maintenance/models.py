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