from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .serializers import ModuleSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.db.models.query_utils import Q
from .models import Module


# Create your views here.
class StandardResultSetPagination(PageNumberPagination):
    page_size = 6  # Default number of records per page when not specified
    page_size_query_param = 'page_size'
    max_page_size = 6  # Max Limit


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return Module.objects.filter()

    def perform_create(self, serializer):
        serializer.save()
