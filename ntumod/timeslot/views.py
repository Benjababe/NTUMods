from .models import TimeSlot
from rest_framework import viewsets, filters, generics
from .serializers import VenueTimeSlotSerializer


class VenueTimeSlotViewSet(generics.ListAPIView):
    serializer_class = VenueTimeSlotSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TimeSlot.objects.all()

        venue_id = self.request.query_params.get('venue_id')

        if venue_id is not None:
            queryset = queryset.filter(venue_id=venue_id)

        return queryset
