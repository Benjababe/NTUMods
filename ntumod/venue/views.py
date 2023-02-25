from django.db.models import Count
from django.db.models.query_utils import Q
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Venue
from .serializers import VenueSerializer


# Create your views here.
class StandardResultSetPagination(PageNumberPagination):
    page_size = 15  # Default number of records per page when not specified
    page_size_query_param = 'page_size'
    max_page_size = 15  # Max Limit


class VenueViewSet(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return Venue.objects.filter().order_by('name')

    def perform_create(self, serializer):
        serializer.save()
