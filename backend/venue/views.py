from django.db.models.functions import Cast, Sqrt, Power
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param

from django.db.models import Q, F, FloatField

from .models import Venue
from .serializers import VenueSerializer
from timeslot.models import TimeSlot

import datetime

earth_radius_m = 6371000

# Create your views here.
class StandardResultSetPagination(PageNumberPagination):
    page_size = 26  # Default number of records per page when not specified
    page_size_query_param = 'page_size'
    max_page_size = 26  # Max Limit

    def get_next_link(self):
        if not self.page.has_next():
            return None
        
        url = self.request.build_absolute_uri()
        scheme = self.request.is_secure() and "https" or "http"
        fwd_scheme = self.request.META.get("HTTP_X_FORWARDED_PROTO")
        is_secure = (scheme == "https" or fwd_scheme == "https")

        new_url = url.replace(f"http://", "https://", 1) if is_secure else url
        page_number = self.page.next_page_number()
        return replace_query_param(new_url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        
        url = self.request.build_absolute_uri()
        scheme = self.request.is_secure() and "https" or "http"
        fwd_scheme = self.request.META.get("HTTP_X_FORWARDED_PROTO")
        is_secure = (scheme == "https" or fwd_scheme == "https")

        new_url = url.replace(f"http://", "https://", 1) if is_secure else url
        page_number = self.page.next_page_number()
        return replace_query_param(new_url, self.page_query_param, page_number)


class VenueViewSet(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return Venue.objects.filter().order_by('name')

    def perform_create(self, serializer):
        serializer.save()


class VenueSearchViewSet(generics.ListAPIView):
    serializer_class = VenueSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        queryset = Venue.objects.all().order_by('name')

        venue_name = self.request.query_params.get('name')

        if venue_name is not None:
            queryset = queryset.filter(name__icontains=venue_name)

        return queryset


class VenueFreeSearchViewSet(generics.ListAPIView):
    serializer_class = VenueSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        # Free time slot wanted
        start_time = datetime.time(int(self.request.query_params.get('start')), 0, 0)
        end_time = datetime.time(int(self.request.query_params.get('end')), 0, 0)
        day = str(self.request.query_params.get('day'))

        # Current location of user
        long = self.request.query_params.get('long')
        lat = self.request.query_params.get('lat')

        # Get the entire list of venue that are not available
        rooms_not_available_list = TimeSlot.objects.filter(
            Q(time_start__lt=end_time) &
            Q(time_end__gt=start_time) &
            Q(day=day)
        ).values_list('venue', flat=True)

        # Exclude all the venue that are not available
        available_rooms_qs = Venue.objects.exclude(id__in=rooms_not_available_list)

        # Compute the distance for each venue to given long lat and then
        # order venue by ascending order of distance
        if long is not None and lat is not None:
            available_rooms_ordered_qs = available_rooms_qs.annotate(
                    distance=Cast(
                        earth_radius_m * Sqrt(
                            Power(F('lat') - long, 2) +
                            Power(F('long') - lat, 2)
                        ),
                        output_field=FloatField()
                    )
                ).order_by('distance')

            return available_rooms_ordered_qs

        return available_rooms_qs
