from rest_framework import serializers
from .models import TimeSlot


class VenueTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'
