from rest_framework import serializers
from .models import Venue
from timeslot.models import TimeSlot

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
