from django.db import models


# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    long = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
