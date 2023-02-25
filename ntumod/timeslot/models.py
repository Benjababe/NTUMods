from django.db import models

# Create your models here.
from venue.models import Venue
from course_module.models import Module


class TimeSlot(models.Model):
    type = models.CharField(max_length=10, null=True, blank=True)
    group = models.CharField(max_length=10, null=True, blank=True)
    day = models.CharField(max_length=4, null=True, blank=True)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)