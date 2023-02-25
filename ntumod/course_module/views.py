from operator import or_

from django.db.models import Count
from django.db.models.query_utils import Q
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Module
from .serializers import ModuleSerializer


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
        return Module.objects.filter().order_by('code')

    def perform_create(self, serializer):
        serializer.save()


class ModuleSearchViewSet(generics.ListAPIView):
    serializer_class = ModuleSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        queryset = Module.objects.all().order_by('code')

        query = self.request.query_params.get('query')

        if query is not None:
            queryset = queryset.filter(
                or_(Q(name__icontains=query), Q(code__icontains=query)))

        return queryset
