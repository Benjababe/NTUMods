from django.db import models


# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    lat = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    long = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'ID:{self.pk} : {self.name}'

    class Meta:
        app_label = 'venue'
