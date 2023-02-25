from django.db.models import CharField, Value

from .models import TimeSlot
from venue.models import Venue
from rest_framework import viewsets, filters, generics
from .serializers import VenueTimeSlotSerializer


class VenueTimeSlotViewSet(generics.ListAPIView):
    serializer_class = VenueTimeSlotSerializer

    def get_queryset(self):
        queryset = TimeSlot.objects.all()

        venue_id = self.request.query_params.get('venue_id')

        if venue_id is not None:
            queryset = queryset.filter(venue_id=venue_id)

        return queryset
