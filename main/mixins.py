from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PaginatedMixin:
    pagination_class = PageNumberPagination 

    def paginate_queryset(self, queryset):
        paginator = self.pagination_class()
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        return paginator.get_paginated_response(data)
