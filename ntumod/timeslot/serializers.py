from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import TimeSlot


class VenueTimeSlotSerializer(serializers.ModelSerializer):
    venue_name = ReadOnlyField(source='venue.name')
    module_code = ReadOnlyField(source='module.code')
    module_name = ReadOnlyField(source='module.name')

    class Meta:
        model = TimeSlot
        fields = '__all__'
