from rest_framework import filters, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param

from .models import Venue
from .serializers import VenueSerializer


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
