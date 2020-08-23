from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Car(models.Model):
    make = models.CharField(max_length=10)
    model = models.CharField(max_length=10)
    vrn = models.CharField(max_length=10)
    year = models.IntegerField(default=timezone.now().year,
                               validators=[MinValueValidator(timezone.now().year - 100),
                                           MaxValueValidator(timezone.now().year)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.make} {self.model}'


class Repair(models.Model):
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        lead = self.description[:10] + '...'
        return lead
