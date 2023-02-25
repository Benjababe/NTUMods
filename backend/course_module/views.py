from operator import or_

from django.db.models.query_utils import Q
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param

from .models import Module
from .serializers import ModuleSerializer


# Create your views here.
class StandardResultSetPagination(PageNumberPagination):
    page_size = 6  # Default number of records per page when not specified
    page_size_query_param = 'page_size'
    max_page_size = 6  # Max Limit

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
