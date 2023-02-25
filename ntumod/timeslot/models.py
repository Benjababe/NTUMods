from course_module.models import Module
from django.db import models
# Create your models here.
from venue.models import Venue


class TimeSlot(models.Model):
    index = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    group = models.CharField(max_length=10, null=True, blank=True)
    day = models.CharField(max_length=4, null=True, blank=True)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='venue')
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Time Slots"
